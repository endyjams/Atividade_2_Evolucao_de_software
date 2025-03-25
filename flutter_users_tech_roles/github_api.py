import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def get_releases(owner, repo, num_releases=10):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page={num_releases}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    releases = response.json()
    releases.sort(key=lambda r: r["published_at"])
    return releases

def get_contributors_between_releases(owner, repo, tag_prev, tag_curr):
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{tag_prev}...{tag_curr}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    contributors = set()
    for commit in data.get("commits", []):
        if commit.get("author") and commit["author"].get("login"):
            contributors.add(commit["author"]["login"])
    return contributors

def get_user_info(username):
    user_resp = requests.get(f"https://api.github.com/users/{username}", headers=HEADERS)
    user_resp.raise_for_status()
    user_info = user_resp.json()

    repos_resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=50&sort=updated", headers=HEADERS)
    repos_resp.raise_for_status()
    repos = repos_resp.json()

    return {
        "username": username,
        "bio": user_info.get("bio", "") or "",
        "repos": repos
    }
