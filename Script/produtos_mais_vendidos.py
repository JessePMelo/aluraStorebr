import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
urls = [
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"
]

# Leitura e identificação de cada loja
lojas = []
for i, url in enumerate(urls, start=1):
    df = pd.read_csv(url)
    df['Loja'] = f'Loja {i}'
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], dayfirst=True)
    df['Ano'] = df['Data da Compra'].dt.year
    lojas.append(df)

# Concatena tudo
df = pd.concat(lojas, ignore_index=True)

# Parâmetros de plot
anos = [2021, 2022]
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # até 4 lojas
fig, axes = plt.subplots(1, 2, figsize=(18, 6), sharey=True)

for ax, ano in zip(axes, anos):
    # filtra o ano
    df_ano = df[df['Ano'] == ano]
    # conta vendas por produto e loja
    prod_loja = (
        df_ano
        .groupby(['Produto', 'Loja'])
        .size()
        .reset_index(name='Quantidade')
    )
    # pivot para ter lojas como colunas
    tabela = prod_loja.pivot(index='Produto', columns='Loja', values='Quantidade').fillna(0).astype(int)

    # seleciona top 10 produtos mais vendidos (pela soma das lojas)
    soma_total = tabela.sum(axis=1).sort_values(ascending=False)
    top10 = soma_total.head(10).index
    tabela = tabela.loc[top10]

    # plota barras agrupadas
    tabela.plot(kind='bar', ax=ax, color=cores, width=0.8)
    ax.set_title(f'Top 10 Produtos Mais Vendidos — {ano}', fontsize=14)
    ax.set_xlabel('Produto', fontsize=12)
    ax.set_ylabel('Quantidade de Compras', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    ax.legend(title='Loja', fontsize=10, title_fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # rótulos de valor
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', fontsize=8, label_type='edge', padding=1)

plt.tight_layout()
plt.savefig('./Imagens/top10_produtos_mais_vendidos_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()
