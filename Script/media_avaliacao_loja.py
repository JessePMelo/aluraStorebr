import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, FuncFormatter

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

# Dicionário para armazenar a média de avaliação por loja para cada ano
medias_por_ano = {ano: {} for ano in anos}

# Processar cada loja e calcular as médias por ano
for i, loja in enumerate(lojas, start=1):
    for ano in anos:
        media = loja[loja['Data da Compra'].dt.year == ano]['Avaliação da compra'].mean()
        medias_por_ano[ano][f'Loja {i}'] = float(media)

# Preparar dados para o gráfico
nomes_lojas = list(medias_por_ano[anos[0]].keys())
valores_por_ano = {ano: list(medias_por_ano[ano].values()) for ano in anos}

# Criar subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

cores = {anos[0]: 'skyblue', anos[1]: 'lightgreen'}

# Gerar um gráfico para cada ano
for idx, ano in enumerate(anos):
    ax = axes[idx]
    valores = valores_por_ano[ano]
    barras = ax.bar(nomes_lojas, valores, color=cores[ano], edgecolor='black')

    ax.set_title(f'Média de Avaliação por Loja ({ano})', fontsize=14)
    ax.set_xlabel('Lojas')
    ax.set_ylabel('Avaliação Média')
    ax.set_ylim(0, 5)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}'))
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Adicionar valores sobre as barras
    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 0.05,
            f'{valor:.2f}',
            ha='center', va='bottom', fontsize=10
        )

# Ajustar layout e salvar imagem
plt.tight_layout()
plt.savefig('./Imagens/media_por_loja_2022_2023.png', dpi=300, bbox_inches='tight')
plt.show()