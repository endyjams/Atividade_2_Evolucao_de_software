"""
plotting.py

Este módulo contém funções para gerar visualizações:
- Distribuição média dos tópicos nas issues.
- Número de desenvolvedores por release (análise de turnover).
- Gráficos para evidências de gerência de mudanças.
"""

import matplotlib.pyplot as plt

def plot_topic_distribution(lda, tfidf, n_topics=5):
    """
    Plota a distribuição média dos tópicos das issues utilizando o resultado do LDA.
    """
    topic_distribution = lda.transform(tfidf)
    avg_distribution = topic_distribution.mean(axis=0)
    plt.figure(figsize=(8, 5))
    plt.bar(range(n_topics), avg_distribution)
    plt.xlabel("Tópico")
    plt.ylabel("Distribuição Média")
    plt.title("Distribuição Média dos Tópicos nas Issues")
    plt.xticks(range(n_topics))
    plt.show()

def plot_developer_turnover(dev_data):
    """
    Plota um gráfico com o número de desenvolvedores por release.
    """
    releases = [d["release"] for d in dev_data]
    num_devs = [d["num_developers"] for d in dev_data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(releases, num_devs, marker='o')
    plt.title("Número de Desenvolvedores por Release")
    plt.xlabel("Release")
    plt.ylabel("Número de Desenvolvedores")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_change_management_evidence(evidence_list, key):
    """
    Plota a frequência de evidências de um determinado aspecto de mudança (ex: 'impacto', 'documentacao')
    a partir da lista de evidências extraída das issues.
    """
    issue_numbers = [e["issue_number"] for e in evidence_list]
    counts = [e["evidence"].get(key, 0) for e in evidence_list]
    
    plt.figure(figsize=(10, 6))
    plt.bar(issue_numbers, counts)
    plt.xlabel("Issue Number")
    plt.ylabel(f"Contagem de evidência: {key}")
    plt.title(f"Evidências de '{key}' nas Issues")
    plt.show()
