# analysis.py
import pandas as pd
import networkx as nx

def compute_commit_statistics(commits: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estatísticas de commits por desenvolvedor, como número total de commits,
    linhas adicionadas e removidas.
    """
    stats = commits.groupby('author').agg(
        total_commits=('commit_id', 'count'),
        total_lines_added=('lines_added', 'sum'),
        total_lines_removed=('lines_removed', 'sum')
    ).reset_index()
    return stats

def compute_turnover(commits: pd.DataFrame, releases: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a rotatividade de desenvolvedores entre releases.
    Para cada release, identifica os novos desenvolvedores e os que não mais contribuem.
    Retorna um DataFrame com:
    - release, release_date, num_dev_at_release, num_new_dev, num_inactive_dev, turnover_rate.
    """
    releases = releases.sort_values('date')
    turnover_data = []
    prev_devs = set()
    for _, row in releases.iterrows():
        release = row['release']
        rel_date = row['date']
        # Seleciona commits até a data da release
        current_commits = commits[commits['date'] <= rel_date]
        current_devs = set(current_commits['author'].unique())
        new_devs = current_devs - prev_devs
        # Desenvolvedores inativos: últimos commits com diferença maior que 90 dias
        inactive_devs = set()
        for dev in prev_devs:
            dev_commits = commits[commits['author'] == dev]
            if not dev_commits.empty:
                last_commit_date = dev_commits['date'].max()
                if (rel_date - last_commit_date).days > 90:
                    inactive_devs.add(dev)
        turnover_rate = (len(new_devs) + len(inactive_devs)) / max(1, len(current_devs))
        turnover_data.append({
            'release': release,
            'release_date': rel_date,
            'num_dev_at_release': len(current_devs),
            'num_new_dev': len(new_devs),
            'num_inactive_dev': len(inactive_devs),
            'turnover_rate': turnover_rate
        })
        prev_devs = current_devs
    return pd.DataFrame(turnover_data)

def build_collaboration_graph(commits: pd.DataFrame) -> nx.Graph:
    """
    Cria um grafo de colaboração onde os nós são os desenvolvedores.
    Uma aresta é criada entre dois desenvolvedores se eles contribuíram para a mesma release.
    O peso da aresta representa o número de releases em que colaboraram juntos.
    """
    edge_dict = {}
    releases = commits['release'].unique()
    for rel in releases:
        devs = commits[commits['release'] == rel]['author'].unique()
        for i in range(len(devs)):
            for j in range(i+1, len(devs)):
                pair = tuple(sorted([devs[i], devs[j]]))
                edge_dict[pair] = edge_dict.get(pair, 0) + 1

    G = nx.Graph()
    developers = commits['author'].unique()
    G.add_nodes_from(developers)
    for (dev1, dev2), weight in edge_dict.items():
        G.add_edge(dev1, dev2, weight=weight)
    return G

def extract_developer_profiles(commits: pd.DataFrame, issues: pd.DataFrame) -> pd.DataFrame:
    """
    Extrai perfis dos desenvolvedores considerando métricas de atividade em commits e issues.
    Retorna um DataFrame com:
    - author, total_commits, total_lines_added, total_lines_removed,
      total_issues_opened, total_issues_closed.
    """
    commit_stats = commits.groupby('author').agg(
        total_commits=('commit_id', 'count'),
        total_lines_added=('lines_added', 'sum'),
        total_lines_removed=('lines_removed', 'sum')
    ).reset_index()
    
    issue_stats = issues.groupby('author').agg(
        total_issues_opened=('issue_id', 'count'),
        total_issues_closed=('closed_at', lambda x: x.notnull().sum())
    ).reset_index()
    
    profiles = pd.merge(commit_stats, issue_stats, on='author', how='outer').fillna(0)
    profiles['total_commits'] = profiles['total_commits'].astype(int)
    profiles['total_issues_opened'] = profiles['total_issues_opened'].astype(int)
    profiles['total_issues_closed'] = profiles['total_issues_closed'].astype(int)
    return profiles
