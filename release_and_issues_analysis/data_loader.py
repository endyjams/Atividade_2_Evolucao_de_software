# data_loader.py
import pandas as pd

def load_commits(filepath: str) -> pd.DataFrame:
    """
    Carrega os dados de commits.
    Espera-se que o arquivo CSV contenha, ao menos, as colunas:
    commit_id, author, date, release, lines_added, lines_removed.
    """
    df = pd.read_csv(filepath, parse_dates=['date'])
    df['author'] = df['author'].astype(str).str.strip().str.lower()
    return df

def load_issues(filepath: str) -> pd.DataFrame:
    """
    Carrega os dados de issues.
    Espera-se que o arquivo CSV contenha, ao menos, as colunas:
    issue_id, author, created_at, closed_at, labels, release.
    """
    df = pd.read_csv(filepath, parse_dates=['created_at', 'closed_at'])
    df['author'] = df['author'].astype(str).str.strip().str.lower()
    return df

def load_releases(filepath: str) -> pd.DataFrame:
    """
    Carrega os dados de releases.
    Espera-se que o arquivo CSV contenha, ao menos, as colunas:
    release, date, description.
    """
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df
