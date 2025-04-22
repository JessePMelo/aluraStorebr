import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Definir anos de interesse aqui
anos = [2021, 2022]

# Carregar os dados
url1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url1)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

# Adicionar a coluna 'Loja'
loja1["Loja"] = "Loja 1"
loja2["Loja"] = "Loja 2"
loja3["Loja"] = "Loja 3"
loja4["Loja"] = "Loja 4"

# Unir os dados
lojas = pd.concat([loja1, loja2, loja3, loja4], ignore_index=True)

# Converter datas e extrair o ano
lojas['Data da Compra'] = pd.to_datetime(lojas['Data da Compra'], dayfirst=True)
lojas['Ano'] = lojas['Data da Compra'].dt.year

# Filtrar apenas os anos definidos
df_filtered = lojas[lojas['Ano'].isin(anos)]

# Calcular média de parcelas por loja e ano
mean_parcelas = (
    df_filtered
    .groupby(['Loja', 'Ano'])['Quantidade de parcelas']
    .mean()
    .unstack()
    .loc[:, anos]
)

# Plot agrupado
lojas_nomes = mean_parcelas.index.tolist()
x = np.arange(len(lojas_nomes))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
for idx, ano in enumerate(anos):
    ax.bar(x + idx*width, mean_parcelas[ano], width, label=str(ano))

ax.set_title(f'Média de Parcelas por Loja ({anos[0]} vs. {anos[1]})', fontsize=14)
ax.set_xlabel('Loja', fontsize=12)
ax.set_ylabel('Média de Quantidade de Parcelas', fontsize=12)
ax.set_xticks(x + width*(len(anos)-1)/2)
ax.set_xticklabels(lojas_nomes, rotation=0, fontsize=10)
ax.legend(title='Ano', fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Adicionar valores nas barras
for idx, ano in enumerate(anos):
    for xi, val in zip(x + idx*width, mean_parcelas[ano]):
        ax.text(xi, val + 0.05, f'{val:.2f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f"./Imagens/media_parcela_lojas_{anos[0]}_{anos[1]}.png", dpi=300, bbox_inches="tight")
plt.show()