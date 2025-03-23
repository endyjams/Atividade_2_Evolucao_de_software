import json
import matplotlib.pyplot as plt
from collections import defaultdict


# Função para carregar os dados do arquivo JSON
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line.strip()) for line in file]


# Função para calcular a atividade por período
def calculate_activity(data):
    # Armazenando os resultados
    activity_by_period = defaultdict(lambda: {'commits': 0, 'issues': 0, 'pulls': 0})
    developers_active_by_period = defaultdict(set)

    # Processando os dados
    for entry in data:
        developer = entry['developer']
        period = entry['period']
        commits = entry['commits']
        issues = entry['issues']
        pulls = entry['pulls']

        # Atualizando os contadores para cada período
        activity_by_period[period]['commits'] += commits
        activity_by_period[period]['issues'] += issues
        activity_by_period[period]['pulls'] += pulls

        # Registrando o desenvolvedor ativo no período
        developers_active_by_period[period].add(developer)

    # Calcular o número de desenvolvedores ativos por período
    activity_metrics = []
    for period, activity in activity_by_period.items():
        active_devs = len(developers_active_by_period[period])
        total_activity = activity['commits'] + activity['issues'] + activity['pulls']
        activity_metrics.append({
            'period': period,
            'active_devs': active_devs,
            'commits': activity['commits'],
            'issues': activity['issues'],
            'pulls': activity['pulls'],
            'total_activity': total_activity
        })

    return activity_metrics


# Função para gerar o gráfico
def plot_activity_graph(activity_metrics):
    # Ordenando os dados pela data (período)
    activity_metrics.sort(key=lambda x: x['period'])

    # Coletando os dados para o gráfico
    periods = [metric['period'] for metric in activity_metrics]
    commits = [metric['commits'] for metric in activity_metrics]
    issues = [metric['issues'] for metric in activity_metrics]
    pulls = [metric['pulls'] for metric in activity_metrics]
    total_activity = [metric['total_activity'] for metric in activity_metrics]

    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(periods, commits, label='Commits', marker='o', linestyle='-', color='b')
    ax.plot(periods, issues, label='Issues', marker='s', linestyle='-', color='g')
    ax.plot(periods, pulls, label='Pulls', marker='^', linestyle='-', color='r')
    ax.plot(periods, total_activity, label='Atividade Total', marker='d', linestyle='-', color='purple')

    # Adicionando título e rótulos
    ax.set_title('Atividade por Período de Desenvolvedores no Projeto')
    ax.set_xlabel('Período')
    ax.set_ylabel('Quantidade de Atividade')
    ax.legend()

    # Melhorando a visibilidade das labels do eixo X
    plt.xticks(rotation=45, ha='right')

    # Selecionando a cada 3 períodos para exibir a data
    ticks_to_show = periods[::3]
    ax.set_xticks(ticks_to_show)
    ax.set_xticklabels(ticks_to_show, rotation=45, ha='right', fontsize=10)

    # Exibindo o gráfico
    plt.tight_layout()
    plt.show()


# Caminho para o arquivo JSON
file_path = 'developer_activity.json'

# Carregando os dados do arquivo
data = load_data_from_json(file_path)

# Calculando a atividade mensal
activity_metrics = calculate_activity(data)

# Gerando o gráfico com os resultados
plot_activity_graph(activity_metrics)
