import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
url1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url1)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

# Adicionar a coluna 'Loja' antes da união
loja1["Loja"] = "Loja 1"
loja2["Loja"] = "Loja 2"
loja3["Loja"] = "Loja 3"
loja4["Loja"] = "Loja 4"

# Concatenar todas as lojas
df_all = pd.concat([loja1, loja2, loja3, loja4], ignore_index=True)

# Consolidar dados por ano
df_all['Ano'] = pd.to_datetime(df_all['Data da Compra']).dt.year

# Função para plotar gráficos por ano com subplots
def plot_estados_comparados(anos):
    n = len(anos)  # Número de gráficos
    fig, axes = plt.subplots(1, n, figsize=(16, 8))  # 1 linha e n colunas
    if n == 1:
        axes = [axes]  # Garantir que axes seja uma lista, mesmo com um gráfico

    for i, ano in enumerate(anos):
        # Filtrar ano
        df_ano = df_all[df_all['Ano'] == ano]

        # Agrupar por loja e estado
        grupado = df_ano.groupby(['Local da compra', 'Loja']).size().reset_index(name='Quantidade')

        # Pivotar para deixar estados como índice e lojas como colunas
        pivot = grupado.pivot(index='Local da compra', columns='Loja', values='Quantidade').fillna(0).astype(int)

        # Ordenar por total geral (somando todas as lojas)
        pivot['Total'] = pivot.sum(axis=1)
        pivot = pivot.sort_values(by='Total', ascending=False).drop(columns='Total')

        # Plotar no subgráfico correspondente
        ax = axes[i]
        pivot.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title(f'Compras por Estado — {ano}', fontsize=16)
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Compras')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Loja')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    
    # Salvar o gráfico com o nome no formato solicitado
    anos_str = "_".join(map(str, anos))
    plt.savefig(f"./Imagens/Compras_por_estado_{anos_str}.png", dpi=300, bbox_inches="tight")
    plt.show()

# Digite os anos desejados
anos = [2021, 2022]

# Gerar gráficos para os anos selecionados
plot_estados_comparados(anos)