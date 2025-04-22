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

# Defina os anos desejados aqui
anos = [2021, 2022]

# Lista de DataFrames
lojas = [loja1, loja2, loja3, loja4]

# Preparar dados: adicionar colunas Ano e Loja
for idx, loja in enumerate(lojas, start=1):
    loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'], dayfirst=True)
    loja['Ano'] = loja['Data da Compra'].dt.year
    loja['Loja'] = f'Loja {idx}'

# Concatenar
df_all = pd.concat(lojas, ignore_index=True)

# Filtrar pelos anos definidos
df_filtered = df_all[df_all['Ano'].isin(anos)]

# Função para pivotar
def pivot_parcelas(df):
    return (
        df.groupby(['Categoria do Produto', 'Loja'])['Quantidade de parcelas']
          .mean()
          .unstack(fill_value=0)
    )

# Criar a pivot para cada ano
pivot_anos = {ano: pivot_parcelas(df_filtered[df_filtered['Ano'] == ano]) for ano in anos}

# Plot
fig, axes = plt.subplots(1, len(anos), figsize=(16, 6), sharey=True)

for ax, ano in zip(axes, anos):
    pivot_anos[ano].plot(kind='bar', ax=ax, width=0.8)
    ax.set_title(f'Média de Parcelas por Categoria — {ano}', fontsize=14)
    ax.set_xlabel('Categoria de Produto', fontsize=12)
    ax.set_ylabel('Média de Quantidade de Parcelas', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f"./Imagens/media_parcela_categorias_lojas_{anos[0]}_{anos[-1]}.png", dpi=300, bbox_inches="tight")
plt.show()