import matplotlib.pyplot as plt
import seaborn as sns

def plot_roles_distribution(roles):
    role_counts = roles.value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribuição dos Papéis Técnicos")
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=role_counts.index, y=role_counts.values)
    plt.ylabel("Quantidade")
    plt.xlabel("Papel Técnico")
    plt.title("Quantidade por Papel Técnico")
    plt.xticks(rotation=45)
    plt.show()
