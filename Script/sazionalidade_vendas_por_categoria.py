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

# Mapeamento numérico dos meses para nomes
meses = {
    1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun',
    7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'
}

# Preparar lista de DataFrames com loja e mês
bases = []
for idx, loja in enumerate([loja1, loja2, loja3, loja4], start=1):
    df = loja.copy()
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], dayfirst=True)
    df['Ano'] = df['Data da Compra'].dt.year
    df['Mês'] = df['Data da Compra'].dt.month
    df['Loja'] = f'Loja {idx}'
    bases.append(df)

# Unificar todos os dados
df_all = pd.concat(bases, ignore_index=True)

# Função para plotar as 4 lojas de um ano
def plot_por_ano(anos):
    for ano in anos:
        fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)
        axes = axes.flatten()

        for i, loja_nome in enumerate(['Loja 1', 'Loja 2', 'Loja 3', 'Loja 4']):
            ax = axes[i]
            df_loja = df_all[(df_all['Loja'] == loja_nome) & (df_all['Ano'] == ano)]

            # Agrupar por mês e categoria
            grp = df_loja.groupby(['Mês', 'Categoria do Produto']).size().reset_index(name='Vendas')

            # Pivotar a tabela
            tabela = grp.pivot(index='Mês', columns='Categoria do Produto', values='Vendas')\
                       .fillna(0).astype(int)
            tabela.index = tabela.index.map(meses)

            # Gráfico de barras empilhadas sem a legenda interna
            tabela.plot(kind='bar', stacked=True, ax=ax, width=0.8, legend=False)
            ax.set_title(f'{loja_nome} — {ano}', fontsize=14)
            ax.set_xlabel('Mês', fontsize=12)
            if i % 2 == 0:
                ax.set_ylabel('Quantidade de Vendas', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Adicionar uma legenda global fora do gráfico
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, title='Categoria', bbox_to_anchor=(1.05, 0.5), loc='center left', fontsize=12)

        # Ajustar o layout para evitar sobreposição
        plt.suptitle(f'Sazonalidade de Vendas por Categoria — {ano}', fontsize=16)
        plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar o layout para dar espaço para a legenda
        plt.savefig(f"./Imagens/Sazonalidade de Vendas por Categoria — {ano}.png", dpi=300, bbox_inches="tight")
        plt.show()

# Digite os anos desejados
anos = [2021, 2022]

# Gerar os gráficos para os anos selecionados
plot_por_ano(anos)
