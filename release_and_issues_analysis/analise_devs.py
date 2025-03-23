import json
import matplotlib.pyplot as plt
from collections import defaultdict


# Função para carregar os dados do arquivo JSON
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line.strip()) for line in file]


# Função para contar os desenvolvedores por perfil
def count_developers_by_profile(data):
    profile_counts = defaultdict(int)

    for entry in data:
        profile = entry['profile']
        profile_counts[profile] += 1

    return profile_counts


# Função para gerar o gráfico
def plot_profile_distribution(profile_counts):
    # Separando os perfis e suas contagens
    profiles = list(profile_counts.keys())
    counts = list(profile_counts.values())

    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(profiles, counts, color=['skyblue', 'lightgreen', 'salmon'])

    # Adicionando título e rótulos
    ax.set_title('Distribuição de Desenvolvedores por Perfil')
    ax.set_xlabel('Perfil')
    ax.set_ylabel('Quantidade de Desenvolvedores')

    # Exibindo o gráfico
    plt.tight_layout()
    plt.show()


# Caminho para o arquivo JSON
file_path = 'developer_profiles.json'

# Carregando os dados do arquivo
data = load_data_from_json(file_path)

# Contando os desenvolvedores por perfil
profile_counts = count_developers_by_profile(data)

# Gerando o gráfico com os resultados
plot_profile_distribution(profile_counts)
