import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

# Lista com os DataFrames das lojas e nomes
lojas = [loja1, loja2, loja3, loja4]
nomes_lojas = [f'Loja {i+1}' for i in range(len(lojas))]

# Converter datas e adicionar coluna de ano
for loja in lojas:
    loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'], dayfirst=True)
    loja['Ano'] = loja['Data da Compra'].dt.year

# Concatenar todos os DataFrames com índice da loja
df_total = pd.concat(lojas, keys=nomes_lojas, names=['Loja'])

# Definir anos a serem analisados
anos = [2021, 2022]

# Definir cores
cores = plt.cm.tab20.colors

# Criar os subplots
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

for idx, ano in enumerate(anos):
    # Filtrar dados do ano
    df_ano = df_total[df_total['Ano'] == ano]

    # Agrupar por loja e categoria
    agrupado = df_ano.groupby(['Loja', 'Categoria do Produto']).size().unstack(fill_value=0)

    # Garantir ordem e presença de todas categorias
    categorias = sorted(df_ano['Categoria do Produto'].unique())
    agrupado = agrupado.reindex(columns=categorias, fill_value=0)

    # Plotar gráfico de barras empilhadas
    ax = axes[idx]
    posicoes = np.arange(len(agrupado.index))
    base = np.zeros(len(agrupado.index))

    for i, categoria in enumerate(agrupado.columns):
        valores = agrupado[categoria].values
        barras = ax.bar(posicoes, valores, bottom=base, label=categoria, color=cores[i % len(cores)])

        # Adicionar rótulos nas barras
        for j, barra in enumerate(barras):
            altura = barra.get_height()
            if altura > 0:
                ax.annotate(f'{int(altura)}',
                            xy=(barra.get_x() + barra.get_width() / 2, base[j] + altura / 2),
                            ha='center', va='center', fontsize=8, color='white')

        base += valores

    # Configurações do gráfico
    ax.set_title(f'Vendas por Categoria em {ano}', fontsize=15)
    ax.set_xlabel('Loja', fontsize=12)
    ax.set_xticks(posicoes)
    ax.set_xticklabels(agrupado.index)
    if idx == 0:
        ax.set_ylabel('Quantidade Vendida', fontsize=12)

# Legenda fora do gráfico
axes[1].legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, title_fontsize=10)

# Ajustar layout e salvar imagem
plt.tight_layout()
plt.savefig('./Imagens/vendas_por_categoria_agrupada_proporcional_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()
