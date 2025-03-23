# fetch_data.py
import requests
import pandas as pd
import time
import os

GITHUB_API_BASE = "https://api.github.com"
REPO_OWNER = "flutter"
REPO_NAME = "flutter"
HEADERS = {}
TOKEN = os.getenv("GITHUB_TOKEN")
if TOKEN:
    HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch_commits(max_pages=10, per_page=100):
    """
    Busca os dados de commits do repositório utilizando a API do GitHub.
    Para cada commit, extrai: commit_id, author, data e associa um campo de release (inicialmente None).
    Note que informações de estatísticas (linhas adicionadas/removidas) não estão disponíveis na listagem padrão.
    """
    all_commits = []
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    params = {"per_page": per_page, "page": 1}
    for page in range(1, max_pages+1):
        params["page"] = page
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar commits na página {page}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        for commit in data:
            commit_id = commit.get("sha")
            author = commit.get("commit", {}).get("author", {}).get("name", "unknown")
            date = commit.get("commit", {}).get("author", {}).get("date")
            # As estatísticas (lines_added/lines_removed) não são fornecidas neste endpoint padrão.
            all_commits.append({
                "commit_id": commit_id,
                "author": author,
                "date": date,
                "release": None,  # Para associação futura, se desejado
                "lines_added": None,
                "lines_removed": None
            })
        print(f"Fetched page {page} with {len(data)} commits")
        time.sleep(1)  # Respeitar rate limit
    return pd.DataFrame(all_commits)

def fetch_issues(max_pages=10, per_page=100):
    """
    Busca as issues do repositório. Considera issues de todos os estados.
    Filtra _pull requests_ (eles possuem o campo 'pull_request') para focar apenas em issues.
    """
    all_issues = []
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    params = {"state": "all", "per_page": per_page, "page": 1}
    for page in range(1, max_pages+1):
        params["page"] = page
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar issues na página {page}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        for issue in data:
            # Filtrar pull requests
            if 'pull_request' in issue:
                continue
            issue_id = issue.get("number")
            author = issue.get("user", {}).get("login", "unknown")
            created_at = issue.get("created_at")
            closed_at = issue.get("closed_at")
            labels = [label.get("name") for label in issue.get("labels", [])]
            labels_str = ", ".join(labels)
            all_issues.append({
                "issue_id": issue_id,
                "author": author,
                "created_at": created_at,
                "closed_at": closed_at,
                "labels": labels_str,
                "release": None  # Para associação futura, se desejado
            })
        print(f"Fetched page {page} with {len(data)} issues (filtered PRs)")
        time.sleep(1)
    return pd.DataFrame(all_issues)

def fetch_releases():
    """
    Busca as releases do repositório a partir da API do GitHub.
    Extrai: tag (nome da release), data de publicação e descrição.
    """
    all_releases = []
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    params = {"per_page": 100, "page": 1}
    page = 1
    while True:
        params["page"] = page
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar releases na página {page}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        for release in data:
            release_name = release.get("tag_name")
            release_date = release.get("published_at")
            description = release.get("body")
            all_releases.append({
                "release": release_name,
                "date": release_date,
                "description": description
            })
        print(f"Fetched page {page} with {len(data)} releases")
        page += 1
        time.sleep(1)
    return pd.DataFrame(all_releases)

def save_data(df, filename):
    """
    Salva o DataFrame em um arquivo CSV.
    """
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

def main():
    commits_df = fetch_commits()
    issues_df = fetch_issues()
    releases_df = fetch_releases()

    save_data(commits_df, os.path.join("data", "commits.csv"))
    save_data(issues_df, os.path.join("data", "issues.csv"))
    save_data(releases_df, os.path.join("data", "releases.csv"))

if __name__ == "__main__":
    main()
