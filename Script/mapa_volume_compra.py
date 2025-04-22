import pandas as pd
import folium
import branca.colormap as cm
import numpy as np

# Carregar os dados
url1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url1)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

# Unir os dados
lojas = pd.concat([loja1, loja2, loja3, loja4])

# Garantir que a data esteja no formato datetime e criar coluna de ano
lojas['Data da Compra'] = pd.to_datetime(lojas['Data da Compra'], dayfirst=True)
lojas['Ano'] = lojas['Data da Compra'].dt.year

# Lista dos anos a analisar
anos = [2021, 2022]

# Função para gerar o mapa por ano
def gerar_mapa_por_ano(lojas, ano):
    # Filtrar por ano
    lojas_ano = lojas[lojas['Ano'] == ano]

    # Agrupar por local
    grupo = lojas_ano.groupby(['Local da compra', 'lat', 'lon']).agg({
        'Produto': 'count',
        'Avaliação da compra': 'mean',
        'Frete': ['sum', 'mean']
    }).reset_index()

    grupo.columns = ['Local', 'lat', 'lon', 'Vendas', 'Avaliação média', 'Frete total', 'Frete médio']

    # Criar mapa
    mapa = folium.Map(location=[-14.235, -51.925], zoom_start=4, tiles="CartoDB positron")

    # Escala de cor: azul (alta avaliação) → vermelho (baixa)
    colormap = cm.LinearColormap(
        colors=['red', 'orange', 'yellow', 'lightblue', 'blue'],
        vmin=grupo['Avaliação média'].min(),
        vmax=grupo['Avaliação média'].max(),
        caption='Avaliação Média da Compra'
    )
    mapa.add_child(colormap)

    # Círculos
    for _, row in grupo.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=np.sqrt(row['Vendas']) * 0.8,
            color=colormap(row['Avaliação média']),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(f"""
                <b>Local:</b> {row['Local']}<br>
                <b>Vendas:</b> {int(row['Vendas'])}<br>
                <b>Avaliação média:</b> {row['Avaliação média']:.2f}<br>
                <b>Frete total:</b> R${row['Frete total']:.2f}<br>
                <b>Frete médio:</b> R${row['Frete médio']:.2f}
            """, max_width=300)
        ).add_to(mapa)

    # Legenda explicativa
    legenda_html = f"""
    <div style="position: fixed;
        bottom: 50px; left: 50px; width: 200px; height: auto;
        background-color: white; z-index:9999; font-size:12px;
        border:1px solid grey; border-radius:8px; padding: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        <b>Legenda ({ano}):</b><br>
        <span style='color:blue'>Azul</span> = Avaliação alta<br>
        <span style='color:red'>Vermelho</span> = Avaliação baixa<br>
        Tamanho do círculo = Vendas<br>
        Cor do círculo = Avaliação média
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(legenda_html))

    return mapa

# Gerar mapas para 2022 e 2023
mapa_2022 = gerar_mapa_por_ano(lojas, 2021)
mapa_2023 = gerar_mapa_por_ano(lojas, 2022)

mapa_2022.save('./Html/mapa_avaliacoes_2021.html')
mapa_2023.save('./Html/mapa_avaliacoes_2022.html')

print("Mapas gerados e salvos com sucesso!")
