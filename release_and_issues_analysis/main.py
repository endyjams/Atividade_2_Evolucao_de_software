# main.py
import os
import fetch_data
import data_loader
import analysis
import visualization

def main():
    # Etapa 1: Buscar os dados a partir da API do GitHub e salvar em CSV
    print("Iniciando fetch dos dados da API do GitHub...")
    fetch_data.main()

    # Definir os caminhos dos arquivos CSV
    commits_filepath = os.path.join('data', 'commits.csv')
    issues_filepath = os.path.join('data', 'issues.csv')
    releases_filepath = os.path.join('data', 'releases.csv')
    
    # Etapa 2: Carregar os dados
    print("Carregando os dados...")
    commits = data_loader.load_commits(commits_filepath)
    issues = data_loader.load_issues(issues_filepath)
    releases = data_loader.load_releases(releases_filepath)
    
    # Etapa 3: Análises
    print("Calculando estatísticas de commits e perfis de desenvolvedor...")
    commit_stats = analysis.compute_commit_statistics(commits)
    developer_profiles = analysis.extract_developer_profiles(commits, issues)
    
    print("Calculando turnover por release...")
    turnover_df = analysis.compute_turnover(commits, releases)
    
    print("Construindo grafo de colaboração...")
    collaboration_graph = analysis.build_collaboration_graph(commits)
    
    # Etapa 4: Visualizações
    if not os.path.exists("results"):
        os.makedirs("results")
    print("Gerando gráficos...")
    visualization.plot_turnover(turnover_df, output_path='results/turnover.png')
    visualization.plot_commit_distribution(developer_profiles, output_path='results/commit_distribution.png')
    visualization.plot_collaboration_graph(collaboration_graph, output_path='results/collaboration_graph.png')
    
    # Resultados básicos no terminal
    print("Estatísticas de Commits por Desenvolvedor:")
    print(commit_stats.head())
    print("\nPerfis de Desenvolvedor:")
    print(developer_profiles.head())
    print("\nTurnover por Release:")
    print(turnover_df.head())
    print("\nAnálise completa realizada. Os gráficos foram salvos na pasta 'results'.")

if __name__ == '__main__':
    main()
