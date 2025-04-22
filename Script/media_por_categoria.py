import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Definir anos a serem analisados
anos = [2021, 2022]

# Calcular média por categoria para cada ano
medias_por_ano = {}
for ano in anos:
    df_ano = df_total[df_total['Ano'] == ano]
    medias_por_ano[ano] = df_ano.groupby('Categoria do Produto')['Avaliação da compra'].mean()

# Obter todas as categorias envolvidas
todas_categorias = sorted(set().union(*[media.index for media in medias_por_ano.values()]))

# Reindexar os dados com todas as categorias
for ano in anos:
    medias_por_ano[ano] = medias_por_ano[ano].reindex(todas_categorias)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

for idx, ano in enumerate(anos):
    ax = axes[idx]
    ax.bar(todas_categorias, medias_por_ano[ano], color='skyblue' if ano == 2022 else 'lightgreen')
    ax.set_title(f'Avaliação Média por Categoria em {ano}', fontsize=14)
    ax.set_xlabel('Categoria', fontsize=12)
    if idx == 0:
        ax.set_ylabel('Avaliação Média', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

# Ajustar layout e salvar imagem
plt.tight_layout()
plt.savefig('./Imagens/media_por_categoria_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()