import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Unir os dados
lojas = pd.concat([loja1, loja2, loja3, loja4], ignore_index=True)

# Converter data e extrair o ano
lojas['Data da Compra'] = pd.to_datetime(lojas['Data da Compra'], dayfirst=True)
lojas['Ano'] = lojas['Data da Compra'].dt.year

# Filtrar apenas os anos de interesse
anos = [2021, 2022]
df_all = lojas[lojas['Ano'].isin(anos)]

# Cores para as lojas
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Criar subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

for ax, ano in zip(axes, anos):
    df_ano = df_all[df_all['Ano'] == ano]

    # Contar compras por tipo de pagamento e loja
    grp = (
        df_ano.groupby(['Tipo de pagamento', 'Loja'])
        .size()
        .reset_index(name='Contagem')
    )

    # Pivot para colocar as lojas como colunas
    tabela = grp.pivot(index='Tipo de pagamento', columns='Loja', values='Contagem')\
               .fillna(0).astype(int)

    # Plot de barras agrupadas
    x = np.arange(len(tabela))
    width = 0.2
    for i, loja in enumerate(tabela.columns):
        ax.bar(x + i * width, tabela[loja], width, label=loja, color=cores[i])

    ax.set_title(f'Métodos de Pagamento em {ano}', fontsize=14)
    ax.set_xlabel('Método de Pagamento', fontsize=12)
    if ano == 2021:
        ax.set_ylabel('Quantidade de Compras', fontsize=12)
    ax.set_xticks(x + width * (len(tabela.columns) - 1) / 2)
    ax.set_xticklabels(tabela.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(title='Loja', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig("./Imagens/metodos_pagamento_lojas_2021_2022.png", dpi=300, bbox_inches="tight")
plt.show()
