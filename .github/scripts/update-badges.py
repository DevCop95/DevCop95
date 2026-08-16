import re
import urllib.request
import json

README = "README.md"

REPOS = [
    "DevCop95/bugbounty-lab101",
]


def get_github_data(repo):
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "readme-updater"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data.get("stargazers_count", 0), data.get("forks_count", 0)


def badge(label, value, color):
    sl = label.replace("-", "--").replace("_", "__").replace(" ", "_")
    sv = str(value).replace("-", "--").replace("_", "__").replace(" ", "_")
    return (
        f"https://img.shields.io/badge/{sl}-{sv}-{color}"
        f"?style=for-the-badge&logo=github&labelColor=0d1117"
    )


def main():
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content

    for repo in REPOS:
        stars, forks = get_github_data(repo)

        stars_url = badge("Stars", stars, "ef4444")
        forks_url = badge("Forks", forks, "494649")

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

    if updated != content:
        with open(README, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"README updated with fresh badge data")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
