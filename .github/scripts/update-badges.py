import re
import urllib.request
import json
import os
import time

README = "README.md"

REPOS = [
    "DevCop95/bugbounty-lab101",
    "DevCop95/shodan_reconsx",
    "DevCop95/pullgoscript",
    "DevCop95/cyhber-deploy",
    "DevCop95/cYHBeriteratus",
]


def get_github_data(repo):
    url = f"https://api.github.com/repos/{repo}"
    headers = {"User-Agent": "readme-updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        return data.get("stargazers_count", 0), data.get("forks_count", 0)
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
        return None, None


def badge(label, value, color):
    sl = label.replace("-", "--").replace("_", "__").replace(" ", "_")
    sv = str(value).replace("-", "--").replace("_", "__").replace(" ", "_")
    return (
        f"https://img.shields.io/badge/{sl}-{sv}-{color}"
        f"?style=for-the-badge&logo=github&labelColor=0d1117"
    )


def update_cache_busters(text, timestamp):
    # Pattern to match URLs from dynamic card services (github-readme-stats-fast, activity-graph, etc.)
    def repl(match):
        url = match.group(0)
        # Remove any existing cache_bust or t query parameters
        cleaned = re.sub(r'([?&])(?:cache_bust|t)=\d+(&?)', r'\1', url)
        # Clean up any trailing ? or & or consecutive && / ?&
        cleaned = re.sub(r'[?&]&', '&', cleaned)
        cleaned = cleaned.replace('?&', '?').rstrip('?&')
        separator = '&' if '?' in cleaned else '?'
        return f"{cleaned}{separator}cache_bust={timestamp}"

    # Match URLs starting with these services until a quote, space, or closing paren/tag
    pattern = r'https://github-readme-(?:stats-fast|activity-graph)\.vercel\.app/[^\s"\'\)\>]+'
    return re.sub(pattern, repl, text)


def main():
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content
    current_time = int(time.time())

    for repo in REPOS:
        stars, forks = get_github_data(repo)
        if stars is None or forks is None:
            continue

        stars_url = badge("Stars", stars, "ef4444")
        forks_url = badge("Forks", forks, "494649")

        # Specific replacement per repo if linked
        repo_name = repo.split("/")[-1]
        
        # Match stars badge associated with this repo
        stars_pattern = rf'\[!\[Stars\]\(https://img\.shields\.io/badge/Stars-\d+-[a-fA-F0-9]+\?[^\)]+\)\]\((?:https://github\.com/{re.escape(repo)}/stargazers)?\)'
        forks_pattern = rf'\[!\[Forks\]\(https://img\.shields\.io/badge/Forks-\d+-[a-fA-F0-9]+\?[^\)]+\)\]\((?:https://github\.com/{re.escape(repo)}/network/members)?\)'
        
        # General fallback if single repo badge in README
        if repo == "DevCop95/bugbounty-lab101":
            updated = re.sub(
                r"\[!\[Stars\]\(https://img\.shields\.io/badge/Stars-\d+-[a-fA-F0-9]+\?[^\)]+\)\]",
                f"[![Stars]({stars_url})]",
                updated,
            )
            updated = re.sub(
                r"\[!\[Forks\]\(https://img\.shields\.io/badge/Forks-\d+-[a-fA-F0-9]+\?[^\)]+\)\]",
                f"[![Forks]({forks_url})]",
                updated,
            )

    # Apply cache-busting to dynamic cards to force GitHub Camo CDN to refresh
    updated = update_cache_busters(updated, current_time)

    if updated != content:
        with open(README, "w", encoding="utf-8") as f:
            f.write(updated)
        print("README updated with fresh badge data and cache-busting timestamps.")
    else:
        print("README already up to date.")


if __name__ == "__main__":
    main()
