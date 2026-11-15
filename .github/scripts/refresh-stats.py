"""Refresh README stats: generate self-hosted SVG cards and bust badge caches.

Why self-hosted SVGs instead of github-readme-stats Vercel mirrors:
Public `.vercel.app` mirrors share a small pool of PATs and Vercel Hobby bandwidth,
causing them to hit rate limits or go offline every ~10 days. By rendering the
4 cards (`pin-bugbounty-lab101.svg`, `pin-shodan_reconsx.svg`, `github-stats.svg`,
`top-langs.svg`) directly from the GitHub API inside GitHub Actions and storing
them in `assets/stats/`, the profile README never depends on third-party mirrors
and never displays broken images even if an API call transiently fails.
"""

from __future__ import annotations

import html
import json
import math
import os
import re
import sys
import textwrap
import time
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

README = Path("README.md")
STATS_DIR = Path("assets/stats")
USERNAME = "DevCop95"
PINNED_REPOS = ["bugbounty-lab101", "shodan_reconsx"]

# Bucket the cache-buster to the cron window so manual re-dispatches inside the
# same 6h window do not create pointless README commits.
REFRESH_INTERVAL_S = 6 * 60 * 60

DYNAMIC_HOST_RE = re.compile(
    r"https://(?:"
    r"img\.shields\.io/github/"
    r"|komarev\.com/ghpvc/"
    r")[^\s\"'\)>]+"
)

LANG_COLORS = {
    "Python": "#3572A5",
    "PowerShell": "#012456",
    "Shell": "#89e051",
    "Go": "#00ADD8",
    "HTML": "#e34c26",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "CSS": "#563d7c",
    "Dockerfile": "#384d54",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Rust": "#dea584",
    "Java": "#b07219",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Assembly": "#6E4C13",
    "Makefile": "#427819",
    "HCL": "#844FBA",
    "Batchfile": "#C1F12E",
}


def api_headers() -> dict[str, str]:
    headers = {
        "User-Agent": "DevCop95-readme-stats-generator",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str, data: bytes | None = None) -> dict | list:
    req = urllib.request.Request(url, data=data, headers=api_headers())
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_github_data(username: str) -> dict:
    """Fetch user, repo, and language stats via GraphQL with REST fallback."""
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        login
        followers { totalCount }
        contributionsCollection {
          totalCommitContributions
        }
        pullRequests(first: 1) { totalCount }
        issues(first: 1) { totalCount }
        repositoriesContributedTo(first: 1, privacy: PUBLIC, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
          totalCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            name
            description
            isFork
            isPrivate
            stargazerCount
            forkCount
            primaryLanguage { name color }
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name color }
              }
            }
          }
        }
      }
    }
    """
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        try:
            payload = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
            res = fetch_json("https://api.github.com/graphql", data=payload)
            if isinstance(res, dict) and "data" in res and res["data"].get("user"):
                return parse_graphql_user(res["data"]["user"], username)
        except Exception as exc:  # noqa: BLE001
            print(f"::warning::GraphQL query failed ({exc}), falling back to REST API")

    return fetch_rest_fallback(username)


def fetch_total_commits_rest(username: str) -> int | None:
    try:
        url = f"https://api.github.com/search/commits?q=author:{ urllib.parse.quote(username) }"
        req = urllib.request.Request(url, headers=api_headers())
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return int(data.get("total_count", 0))
    except Exception:  # noqa: BLE001
        return None


def parse_graphql_user(user: dict, username: str) -> dict:
    repos = user["repositories"]["nodes"]
    public_repos = [r for r in repos if not r.get("isPrivate")]
    total_stars = sum(r.get("stargazerCount", 0) for r in public_repos)

    cc = user.get("contributionsCollection") or {}
    commits_year = int(cc.get("totalCommitContributions", 0))
    total_commits = fetch_total_commits_rest(username) or commits_year
    if commits_year > total_commits:
        total_commits = commits_year

    lang_totals: dict[str, int] = {}
    lang_colors: dict[str, str] = dict(LANG_COLORS)
    for repo in public_repos:
        if repo.get("isFork"):
            continue
        edges = (repo.get("languages") or {}).get("edges") or []
        for edge in edges:
            node = edge.get("node") or {}
            lname = node.get("name")
            lsize = int(edge.get("size") or 0)
            if not lname or lsize <= 0:
                continue
            lang_totals[lname] = lang_totals.get(lname, 0) + lsize
            if node.get("color"):
                lang_colors[lname] = node["color"]

    repo_map = {}
    for r in public_repos:
        pl = r.get("primaryLanguage") or {}
        lname = pl.get("name") or ""
        lcolor = pl.get("color") or lang_colors.get(lname, "#dc2626")
        repo_map[r["name"]] = {
            "name": r["name"],
            "description": r.get("description") or "",
            "stars": int(r.get("stargazerCount", 0)),
            "forks": int(r.get("forkCount", 0)),
            "language": lname,
            "language_color": lcolor,
        }

    return {
        "total_stars": total_stars,
        "total_commits": total_commits,
        "total_prs": int((user.get("pullRequests") or {}).get("totalCount", 0)),
        "total_issues": int((user.get("issues") or {}).get("totalCount", 0)),
        "contributed_to": int((user.get("repositoriesContributedTo") or {}).get("totalCount", 0)),
        "followers": int((user.get("followers") or {}).get("totalCount", 0)),
        "repos": repo_map,
        "languages": lang_totals,
        "lang_colors": lang_colors,
    }


def fetch_rest_fallback(username: str) -> dict:
    repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100&type=owner")
    assert isinstance(repos, list)
    total_stars = sum(int(r.get("stargazers_count", 0)) for r in repos)
    lang_totals: dict[str, int] = {}
    repo_map = {}

    for r in repos:
        name = r["name"]
        lang = r.get("language") or ""
        repo_map[name] = {
            "name": name,
            "description": r.get("description") or "",
            "stars": int(r.get("stargazers_count", 0)),
            "forks": int(r.get("forks_count", 0)),
            "language": lang,
            "language_color": LANG_COLORS.get(lang, "#dc2626"),
        }
        if not r.get("fork"):
            try:
                ldata = fetch_json(f"https://api.github.com/repos/{username}/{name}/languages")
                if isinstance(ldata, dict):
                    for k, v in ldata.items():
                        lang_totals[k] = lang_totals.get(k, 0) + int(v)
            except Exception:  # noqa: BLE001
                pass

    total_commits = fetch_total_commits_rest(username) or 0
    prs = 0
    issues = 0
    try:
        pr_res = fetch_json(f"https://api.github.com/search/issues?q=author:{username}+type:pr")
        if isinstance(pr_res, dict):
            prs = int(pr_res.get("total_count", 0))
        is_res = fetch_json(f"https://api.github.com/search/issues?q=author:{username}+type:issue")
        if isinstance(is_res, dict):
            issues = int(is_res.get("total_count", 0))
    except Exception:  # noqa: BLE001
        pass

    return {
        "total_stars": total_stars,
        "total_commits": total_commits,
        "total_prs": prs,
        "total_issues": issues,
        "contributed_to": 0,
        "followers": 0,
        "repos": repo_map,
        "languages": lang_totals,
        "lang_colors": dict(LANG_COLORS),
    }


def fmt_num(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def render_pin_card(repo: dict) -> str:
    """Render a 400x120 repository pin card matching github-readme-stats styling."""
    name = html.escape(repo["name"])
    desc = repo["description"] or "No description provided."
    lines = textwrap.wrap(desc, width=52)[:2]
    if len(lines) == 2 and len(desc) > sum(len(x) for x in lines) + 2:
        lines[1] = lines[1][:49].rstrip() + "..."
    line1 = html.escape(lines[0]) if lines else ""
    line2 = html.escape(lines[1]) if len(lines) > 1 else ""

    lang = html.escape(repo["language"] or "Code")
    lang_color = repo["language_color"] or "#dc2626"
    stars = fmt_num(repo["stars"])
    forks = fmt_num(repo["forks"])

    height = 130 if line2 else 115
    meta_y = height - 22

    desc_svg = f'<text x="25" y="55" class="desc">{line1}</text>'
    if line2:
        desc_svg += f'\n  <text x="25" y="73" class="desc">{line2}</text>'

    # Calculate x offsets for stars and forks
    star_x = 25 + 16 + len(lang) * 7.2 + 18
    fork_x = star_x + 22 + len(stars) * 7.5 + 18

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="{height}" viewBox="0 0 400 {height}" fill="none" role="img" aria-label="{name}">
  <style>
    .title {{ font: 600 15px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #dc2626; }}
    .desc {{ font: 400 12px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c9d1d9; }}
    .meta {{ font: 400 12px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c9d1d9; }}
  </style>
  <rect width="399" height="{height - 1}" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
  <g transform="translate(25, 18)">
    <svg fill="#dc2626" viewBox="0 0 16 16" width="16" height="16" y="0">
      <path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
    </svg>
    <text x="24" y="13" class="title">{name}</text>
  </g>
  {desc_svg}
  <g transform="translate(0, {meta_y})">
    <circle cx="30" cy="-4" r="5" fill="{lang_color}"/>
    <text x="41" y="0" class="meta">{lang}</text>
    <g transform="translate({star_x:.0f}, -13)">
      <svg fill="#dc2626" viewBox="0 0 16 16" width="15" height="15">
        <path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"/>
      </svg>
      <text x="19" y="13" class="meta">{stars}</text>
    </g>
    <g transform="translate({fork_x:.0f}, -13)">
      <svg fill="#dc2626" viewBox="0 0 16 16" width="15" height="15">
        <path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"/>
      </svg>
      <text x="19" y="13" class="meta">{forks}</text>
    </g>
  </g>
</svg>
"""


def render_github_stats_card(data: dict) -> str:
    """Render the GitHub Stats card matching theme=tokyonight + rank_icon=github."""
    stars = fmt_num(data["total_stars"])
    commits = fmt_num(data["total_commits"])
    prs = fmt_num(data["total_prs"])
    issues = fmt_num(data["total_issues"])
    contribs = fmt_num(data["contributed_to"])

    rows = [
        (
            "Total Stars Earned:",
            stars,
            "M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z",
        ),
        (
            "Total Commits:",
            commits,
            "M1.643 3.143L.427 1.927A.25.25 0 000 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 00.177-.427L2.715 4.215a6.5 6.5 0 11-1.18 4.458.75.75 0 10-1.493.154 8.001 8.001 0 101.6-5.684zM7.75 4a.75.75 0 01.75.75v2.992l2.028.812a.75.75 0 01-.557 1.392l-2.5-1A.75.75 0 017 8.25v-3.5A.75.75 0 017.75 4z",
        ),
        (
            "Total PRs:",
            prs,
            "M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z",
        ),
        (
            "Total Issues:",
            issues,
            "M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z",
        ),
        (
            "Contributed to:",
            contribs,
            "M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z",
        ),
    ]

    row_svgs = []
    for idx, (label, val, icon_path) in enumerate(rows):
        y = 62 + idx * 25
        row_svgs.append(
            f"""  <g transform="translate(25, {y})">
    <svg fill="#dc2626" viewBox="0 0 16 16" width="16" height="16" y="-12">
      <path fill-rule="evenodd" d="{icon_path}"/>
    </svg>
    <text x="25" y="0" class="label">{label}</text>
    <text x="215" y="0" class="val">{val}</text>
  </g>"""
        )

    rows_block = "\n".join(row_svgs)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="450" height="195" viewBox="0 0 450 195" fill="none" role="img" aria-label="DevCop95's GitHub Stats">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #dc2626; }}
    .label {{ font: 600 13.5px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c9d1d9; }}
    .val {{ font: 700 13.5px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c9d1d9; }}
  </style>
  <rect width="449" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
  <text x="25" y="34" class="header">DevCop95's GitHub Stats</text>
{rows_block}
  <g transform="translate(365, 108)">
    <circle cx="0" cy="0" r="40" stroke="#21262d" stroke-width="6" fill="none"/>
    <circle cx="0" cy="0" r="40" stroke="#dc2626" stroke-width="6" stroke-dasharray="225 252" stroke-linecap="round" transform="rotate(-90)" fill="none"/>
    <svg fill="#c9d1d9" viewBox="0 0 16 16" width="40" height="40" x="-20" y="-20">
      <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
    </svg>
  </g>
</svg>
"""


def render_top_langs_card(data: dict, count: int = 8) -> str:
    """Render the Compact Most Used Languages card matching theme=tokyonight."""
    langs = sorted(data["languages"].items(), key=lambda kv: kv[1], reverse=True)[:count]
    total = sum(size for _, size in langs) or 1
    colors = data["lang_colors"]

    bar_width = 300
    bar_x = 25
    bar_y = 50
    curr_x = float(bar_x)
    segments = []
    for idx, (name, size) in enumerate(langs):
        pct = size / total
        w = max(2.0, round(pct * bar_width, 2))
        if idx == len(langs) - 1:
            w = max(2.0, round((bar_x + bar_width) - curr_x, 2))
        color = colors.get(name, "#dc2626")
        segments.append(
            f'    <rect x="{curr_x:.2f}" y="{bar_y}" width="{w:.2f}" height="8" fill="{color}"/>'
        )
        curr_x += w

    legend = []
    for idx, (name, size) in enumerate(langs):
        pct = (size / total) * 100
        col = idx % 2
        row = idx // 2
        lx = 25 + col * 150
        ly = 82 + row * 25
        color = colors.get(name, "#dc2626")
        safe_name = html.escape(name)
        legend.append(
            f"""  <g transform="translate({lx}, {ly})">
    <circle cx="5" cy="-4" r="5" fill="{color}"/>
    <text x="16" y="0" class="lang">{safe_name} <tspan class="pct">{pct:.2f}%</tspan></text>
  </g>"""
        )

    segments_block = "\n".join(segments)
    legend_block = "\n".join(legend)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="350" height="195" viewBox="0 0 350 195" fill="none" role="img" aria-label="Most Used Languages">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #dc2626; }}
    .lang {{ font: 600 12px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c9d1d9; }}
    .pct {{ font: 400 11.5px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #8b949e; }}
  </style>
  <rect width="349" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
  <text x="25" y="34" class="header">Most Used Languages</text>
  <defs>
    <clipPath id="bar-clip">
      <rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="8" rx="4"/>
    </clipPath>
  </defs>
  <g clip-path="url(#bar-clip)">
{segments_block}
  </g>
{legend_block}
</svg>
"""


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            if path.read_text(encoding="utf-8") == content:
                return False
        except OSError:
            pass
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def bust(url: str, timestamp: int) -> str:
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != "v"]
    query.append(("v", str(timestamp)))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def update_readme(text: str, timestamp: int) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match) -> str:
        nonlocal count
        original = match.group(0)
        refreshed = bust(original, timestamp)
        if refreshed != original:
            count += 1
        return refreshed

    return DYNAMIC_HOST_RE.sub(repl, text), count


def main() -> int:
    try:
        original = README.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"::error::cannot read {README}: {exc}", file=sys.stderr)
        return 1

    # 1. Generate self-hosted SVG stat cards from live GitHub API data
    svg_changed = 0
    try:
        gh_data = fetch_github_data(USERNAME)
        for repo_name in PINNED_REPOS:
            repo_info = gh_data["repos"].get(repo_name)
            if repo_info:
                svg = render_pin_card(repo_info)
                if write_if_changed(STATS_DIR / f"pin-{repo_name}.svg", svg):
                    svg_changed += 1
                print(
                    f"{USERNAME}/{repo_name}: "
                    f"stars={repo_info['stars']} forks={repo_info['forks']}"
                )
        if write_if_changed(STATS_DIR / "github-stats.svg", render_github_stats_card(gh_data)):
            svg_changed += 1
        if write_if_changed(STATS_DIR / "top-langs.svg", render_top_langs_card(gh_data)):
            svg_changed += 1
        print(f"SVG stat cards updated: {svg_changed} file(s) changed.")
    except Exception as exc:  # noqa: BLE001
        print(f"::warning::Failed to refresh SVG cards ({exc}); keeping existing SVGs on disk.")

    # 2. Refresh shields.io / komarev cache-buster on README
    timestamp = (int(time.time()) // REFRESH_INTERVAL_S) * REFRESH_INTERVAL_S
    updated, count = update_readme(original, timestamp)

    if updated != original:
        README.write_text(updated, encoding="utf-8", newline="")
        print(f"Busted CDN cache on {count} badge URL(s).")
    else:
        print("README badge cache-busters already fresh.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
