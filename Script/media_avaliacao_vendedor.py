import pandas as pd
import matplotlib.pyplot as plt

# Lista com os DataFrames das lojas e nomes
urls = [
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"
]

# Recarregar os dados e adicionar as colunas de data e ano
lojas = []
for url in urls:
    df = pd.read_csv(url)
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], dayfirst=True)
    df['Ano'] = df['Data da Compra'].dt.year
    lojas.append(df)

# Concatenar todos os DataFrames com índice da loja
nomes_lojas = [f'Loja {i+1}' for i in range(len(lojas))]
df_total = pd.concat(lojas, keys=nomes_lojas, names=['Loja'])

# Lista dos anos a analisar
anos = [2021, 2022]

# Lista para armazenar os DataFrames agrupados de cada loja
df_avaliacoes = []

# Agrupamento por loja, vendedor e ano
for i, loja in enumerate(lojas, start=1):
    loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'], dayfirst=True)
    loja['Ano'] = loja['Data da Compra'].dt.year
    loja['Loja'] = f'Loja {i}'

    agrupado = loja.groupby(['Loja', 'Vendedor', 'Ano'])['Avaliação da compra'].mean().reset_index()
    df_avaliacoes.append(agrupado)

# Unir todos os dados em um único DataFrame
df_media_avaliacao = pd.concat(df_avaliacoes, ignore_index=True)

# Criar figura com subplots
fig, axes = plt.subplots(1, len(anos), figsize=(14, 6))

# Plotar gráficos dinamicamente para cada ano
for idx, ano in enumerate(anos):
    ax = axes[idx]
    df_ano = df_media_avaliacao[df_media_avaliacao['Ano'] == ano]
    df_pivot = df_ano.pivot_table(index='Vendedor', columns='Loja', values='Avaliação da compra')

    df_pivot.plot(kind='bar', ax=ax, width=0.8, colormap='coolwarm')

    ax.set_title(f'Média de Avaliação de {ano}', fontsize=14)
    ax.set_xlabel('Vendedor', fontsize=12)
    ax.set_ylabel('Média de Avaliação', fontsize=12)
    ax.legend(title='Loja', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

# Ajustar layout
plt.tight_layout()

# Salvar como imagem
plt.savefig('./Imagens/media_de_avaliacao_vendedor_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()