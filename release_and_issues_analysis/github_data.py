"""
github_data.py

Este módulo contém funções para:
- Buscar issues, releases e commits do repositório GitHub.
- Analisar a rotatividade dos desenvolvedores por release.
"""

import os
import requests

# Configuração do repositório do GitHub (exemplo: repositório Flutter)
GITHUB_REPO = "flutter/flutter"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

def get_issues(state="closed", per_page=100):
    """
    Busca issues do repositório com o estado especificado.
    Retorna uma lista de issues.
    """
    url = f"{GITHUB_API_URL}/issues?state={state}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao buscar issues:", response.status_code)
        return []

def get_releases():
    """
    Busca todas as releases do repositório e retorna as 10 últimas ordenadas pela data de publicação.
    """
    url = f"{GITHUB_API_URL}/releases"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        releases = response.json()
        # Ordena pelas releases mais recentes
        releases_sorted = sorted(releases, key=lambda r: r.get('published_at', ""), reverse=True)[:10]
        return releases_sorted
    else:
        print("Erro ao buscar releases:", response.status_code)
        return []

def get_commits_by_release(tag, per_page=100):
    """
    Busca commits associados a uma release utilizando o tag.
    Retorna uma lista de commits para a release especificada.
    """
    url = f"{GITHUB_API_URL}/commits?sha={tag}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao buscar commits para a release", tag, response.status_code)
        return []

def analyze_developer_turnover(releases):
    """
    Para cada release, busca os commits associados e extrai os nomes dos desenvolvedores (autores dos commits).
    Retorna uma lista de dicionários com a tag da release, número de desenvolvedores e a lista dos nomes.
    """
    release_dev_data = []
    for release in releases:
        tag = release.get("tag_name")
        commits = get_commits_by_release(tag)
        authors = set()
        for commit in commits:
            author_info = commit.get("commit", {}).get("author", {})
            name = author_info.get("name")
            if name:
                authors.add(name)
        release_dev_data.append({
            "release": tag,
            "num_developers": len(authors),
            "developers": list(authors)
        })
    return release_dev_data
