"""
main.py

Ponto de entrada do projeto.
Integra as seguintes etapas:
1. Coleta de dados do GitHub (issues, releases e commits) através do módulo github_data.
2. Pré-processamento e modelagem de tópicos das issues usando o módulo text_processing.
3. Extração de evidências de gerência de mudanças a partir das issues com o módulo change_management.
4. Análise da rotatividade de desenvolvedores por release.
5. Visualização dos dados com o módulo plotting.

Para execução:
    python main.py
"""

from github_data import get_issues, get_releases, analyze_developer_turnover
from text_processing import extract_issue_texts, perform_topic_modeling, display_topics, count_keywords
from change_management import extract_change_management_evidence
from plotting import plot_topic_distribution, plot_developer_turnover, plot_change_management_evidence

def main():
    print("===== Coleta de Dados do GitHub =====")
    issues = get_issues()
    if not issues:
        print("Nenhuma issue encontrada.")
        return
    releases = get_releases()
    if releases:
        print("Últimas 10 releases:")
        for release in releases:
            print(f"Release: {release.get('name')} | Tag: {release.get('tag_name')} | Publicado em: {release.get('published_at')}")
    else:
        print("Nenhuma release encontrada.")
    
    print("\n===== Análise de Discussões de Valor e Gerência de Mudanças =====")
    # Pré-processamento dos textos das issues
    texts = extract_issue_texts(issues)
    
    # Modelagem de tópicos com LDA (n_topics=5)
    n_topics = 5
    lda, vectorizer, tfidf = perform_topic_modeling(texts, n_topics=n_topics)
    feature_names = vectorizer.get_feature_names_out()
    topics = display_topics(lda, feature_names, n_top_words=10)
    print("Tópicos Identificados:")
    for idx, words in topics.items():
        print(f"Tópico {idx}: {words}")
    
    # Plot da distribuição média dos tópicos
    plot_topic_distribution(lda, tfidf, n_topics=n_topics)
    
    # Contagem de palavras-chave relacionadas a discussões de valor (ex: 'valor', 'impacto', etc.)
    value_keywords = ['valor', 'impacto', 'melhoria', 'feedback', 'qualidade']
    keyword_counts = count_keywords(texts, value_keywords)
    print("Contagem de palavras-chave relacionadas a 'valor':")
    for kw, count in keyword_counts.items():
        print(f"{kw}: {count}")
    
    # Análise de evidências de gerência de mudanças
    evidence_list = extract_change_management_evidence(issues)
    print("\nExemplo de evidência extraída de gerência de mudanças (por issue):")
    for ev in evidence_list[:5]:
        print(f"Issue #{ev['issue_number']}: {ev['evidence']}")
    
    # Plot de evidência para um aspecto específico (ex: 'impacto')
    plot_change_management_evidence(evidence_list, key="impacto")
    
    print("\n===== Análise de Rotatividade de Desenvolvedores =====")
    dev_data = analyze_developer_turnover(releases)
    for data in dev_data:
        print(f"Release: {data['release']} - Número de Desenvolvedores: {data['num_developers']}")
    
    # Plot da rotatividade de desenvolvedores
    plot_developer_turnover(dev_data)
    
    # Aqui você pode salvar os resultados em arquivos (CSV, PDF, etc.) para compor o tutorial e a documentação final.

if __name__ == "__main__":
    main()
