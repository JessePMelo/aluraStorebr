import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

# Lista com as lojas e nomes
lojas = [loja1, loja2, loja3, loja4]
nomes_lojas = [f'Loja {i+1}' for i in range(len(lojas))]
# Lista com os DataFrames das lojas e nomes
lojas = [loja1, loja2, loja3, loja4]
nomes_lojas = [f'Loja {i+1}' for i in range(len(lojas))]

# Definir cores fixas para as lojas
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Anos fixos
anos = [2021, 2022]

# Inicializar os subplots com 2022 à esquerda
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

for idx, ano in enumerate(anos):
    # Filtrar as lojas para o ano atual
    lojas_ano = []
    for loja in lojas:
        loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'], dayfirst=True)
        loja['Ano'] = loja['Data da Compra'].dt.year
        lojas_ano.append(loja[loja['Ano'] == ano])

    # Obter todas as categorias presentes no ano atual
    todas_categorias = sorted(set().union(*[set(loja['Categoria do Produto']) for loja in lojas_ano]))

    # Montar estrutura de dados
    vendas_por_loja = {nome_loja: [] for nome_loja in nomes_lojas}
    for loja_df, nome_loja in zip(lojas_ano, nomes_lojas):
        contagem = loja_df['Categoria do Produto'].value_counts()
        for categoria in todas_categorias:
            vendas_por_loja[nome_loja].append(contagem.get(categoria, 0))

    # Transformar em DataFrame
    df_vendas = pd.DataFrame(vendas_por_loja, index=todas_categorias)

    # Posições e largura das barras
    posicoes = np.arange(len(df_vendas.index))
    largura_barra = 0.2

    # Criar as barras
    for i, nome_loja in enumerate(df_vendas.columns):
        barras = axes[idx].bar(posicoes + i * largura_barra, df_vendas[nome_loja],
                               width=largura_barra, label=nome_loja, color=cores[i])

        # Adicionar os valores em cima das barras
        for barra in barras:
            altura = barra.get_height()
            axes[idx].annotate(f'{int(altura)}',
                               xy=(barra.get_x() + barra.get_width() / 2, altura),
                               xytext=(0, 3),
                               textcoords="offset points",
                               ha='center', va='bottom', fontsize=8)

    # Configurar eixo x e títulos
    axes[idx].set_title(f'Vendas por Categoria em {ano}')
    axes[idx].set_xlabel('Categoria de Produto')
    axes[idx].set_xticks(posicoes + largura_barra * (len(lojas) - 1) / 2)
    axes[idx].set_xticklabels(df_vendas.index, rotation=45)

# Y comum e legenda
axes[0].set_ylabel('Quantidade Vendida')
axes[1].legend(title='Lojas', loc='upper right')

# Ajustar layout
plt.tight_layout()
plt.savefig('./Imagens/vendas_por_categoria_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()
