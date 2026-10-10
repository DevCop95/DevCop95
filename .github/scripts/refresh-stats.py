"""Refresh the dynamic stats badges in README.md.

The badges are already dynamic (shields.io / github-readme-stats resolve the
value on every request), but GitHub's Camo CDN caches the rendered image by
URL. Appending a `v=<timestamp>` query parameter changes the cache key, so the
next page view pulls a fresh render instead of a stale cached copy.

This deliberately does NOT rewrite the numbers into static badge URLs: if this
workflow ever stops running, the badges keep showing live data instead of a
count frozen at the last successful run.
"""

import json
import os
import re
import sys
import time
import urllib.request
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

README = "README.md"

# Bucket the cache-buster to the cron window. Two runs inside the same window
# therefore produce the same URL, so a manual re-dispatch does not create a
# pointless commit when nothing actually changed.
REFRESH_INTERVAL_S = 6 * 60 * 60  # keep in sync with the cron schedule

# Hosts whose URLs are dynamic stat cards worth busting.
DYNAMIC_HOST_RE = re.compile(
    r"https://(?:"
    r"img\.shields\.io/github/"  # shields.io stars/forks/watchers badges
    r"|github-readme-stats\.vercel\.app/"  # official stats + top-langs + pins
    r")[^\s\"'\)>]+"
)

REPO_FROM_SHIELDS_RE = re.compile(
    r"https://img\.shields\.io/github/(?P<metric>[a-z]+)/(?P<owner>[^/]+)/(?P<repo>[^?/\s\"')]+)"
)


def bust(url: str, timestamp: int) -> str:
    """Return `url` with its `v` cache-buster replaced by `timestamp`."""
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


def fetch_json(url: str) -> dict:
    headers = {"User-Agent": "readme-stats-refresh"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read())


def report_live_counts(text: str) -> None:
    """Print the current stars/forks for every repo referenced by a badge."""
    repos = sorted({(m["owner"], m["repo"]) for m in REPO_FROM_SHIELDS_RE.finditer(text)})
    for owner, repo in repos:
        try:
            data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
        except Exception as exc:  # noqa: BLE001 - reporting only, never fail the job
            print(f"::warning::{owner}/{repo}: could not fetch stats ({exc})")
            continue
        print(
            f"{owner}/{repo}: "
            f"stars={data.get('stargazers_count')} "
            f"forks={data.get('forks_count')}"
        )


def main() -> int:
    try:
        with open(README, encoding="utf-8") as handle:
            original = handle.read()
    except OSError as exc:
        print(f"::error::cannot read {README}: {exc}", file=sys.stderr)
        return 1

    timestamp = (int(time.time()) // REFRESH_INTERVAL_S) * REFRESH_INTERVAL_S
    updated, count = update_readme(original, timestamp)

    if updated == original:
        print("README already carries a fresh cache-buster; nothing to commit.")
    else:
        with open(README, "w", encoding="utf-8", newline="") as handle:
            handle.write(updated)
        print(f"Busted CDN cache on {count} stat badge URL(s).")

    report_live_counts(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
