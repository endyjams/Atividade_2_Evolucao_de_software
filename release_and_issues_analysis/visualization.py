# visualization.py
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def plot_turnover(turnover_df: pd.DataFrame, output_path: str = 'results/turnover.png'):
    """
    Plota a taxa de turnover ao longo das releases.
    """
    plt.figure(figsize=(10,6))
    plt.plot(turnover_df['release_date'], turnover_df['turnover_rate'], marker='o', linestyle='-')
    plt.title('Taxa de Turnover de Desenvolvedores por Release')
    plt.xlabel('Data da Release')
    plt.ylabel('Turnover Rate')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_commit_distribution(profiles: pd.DataFrame, output_path: str = 'results/commit_distribution.png'):
    """
    Plota um histograma da distribuição de commits por desenvolvedor.
    """
    plt.figure(figsize=(10,6))
    plt.hist(profiles['total_commits'], bins=20, edgecolor='black')
    plt.title('Distribuição de Commits por Desenvolvedor')
    plt.xlabel('Número de Commits')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_collaboration_graph(G: nx.Graph, output_path: str = 'results/collaboration_graph.png'):
    """
    Plota o grafo de colaboração entre desenvolvedores.
    """
    plt.figure(figsize=(12,10))
    pos = nx.spring_layout(G, seed=42)
    node_sizes = [100 * G.degree(node) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', alpha=0.9)
    all_weights = [G[u][v]['weight'] for u,v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w*0.5 for w in all_weights], alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title('Grafo de Colaboração entre Desenvolvedores')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
