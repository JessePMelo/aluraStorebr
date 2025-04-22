import pandas as pd
import matplotlib.pyplot as plt

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

# Dicionários para armazenar os faturamentos separados por ano
faturamento_ano_passado = {}
faturamento_ano_antepassado = {}

# Definir cores fixas para as lojas
cores_lojas = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

# Ano fixo
anos = [2021, 2022]

for i, loja in enumerate(lojas):
    loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'], dayfirst=True)
    loja['Total'] = loja['Preço'] + loja['Frete']
    loja['Ano'] = loja['Data da Compra'].dt.year

    # Filtrando os dados por ano
    dados_ano_passado = loja[loja['Ano'] == anos[1]]
    dados_ano_antepassado = loja[loja['Ano'] == anos[0]]

    faturamento_ano_passado[nomes_lojas[i]] = dados_ano_passado['Total'].sum()
    faturamento_ano_antepassado[nomes_lojas[i]] = dados_ano_antepassado['Total'].sum()

# Função personalizada para mostrar % e R$
def formatar_autopct(valores):
    def func(pct):
        total = sum(valores)
        valor = pct * total / 100
        return f'{pct:.1f}%\nR${valor:,.2f}'.replace('.', ',')
    return func

# Criar subplots lado a lado, invertendo a ordem dos gráficos
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Gráfico do ano de 2021 (passado)
axes[1].pie(
    faturamento_ano_passado.values(),
    labels=faturamento_ano_passado.keys(),
    autopct=formatar_autopct(list(faturamento_ano_passado.values())),
    startangle=90,
    colors=cores_lojas
)
axes[1].set_title(f'Faturamento por Loja ({anos[1]})')

# Gráfico do ano de 2022 (antepassado)
axes[0].pie(
    faturamento_ano_antepassado.values(),
    labels=faturamento_ano_antepassado.keys(),
    autopct=formatar_autopct(list(faturamento_ano_antepassado.values())),
    startangle=90,
    colors=cores_lojas
)
axes[0].set_title(f'Faturamento por Loja ({anos[0]})')

plt.tight_layout()
plt.savefig('./Imagens/faturamento_lojas_2021_2022.png', dpi=300, bbox_inches='tight')
plt.show()
