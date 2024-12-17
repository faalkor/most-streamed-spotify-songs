import streamlit as st
import folium
import json
import pandas as pd
import chardet
import os
from graph import graph, aroundStreamings
import matplotlib.pyplot as plt


# Header
st.markdown("<h1 style='text-align: center;'>Músicas mais tocadas (2024)</h1>", unsafe_allow_html=True)



# Dataset encoding detect
dataset = os.path.join(os.getcwd(), 'app', 'mostStreamedSpotifySongs2024.csv')
with open(dataset, 'rb') as f:
    result = chardet.detect(f.read())


# Table
st.markdown("## Dados")
df = pd.read_csv(dataset, encoding=result['encoding'])
st.write(df)


# Top viewed songs
st.markdown("### Músicas mais populares")
graph(df)

# Popularidade por Streaming
st.markdown("### Popularidade por Streaming")
aroundStreamings(df)

# Tabela de contagem de artistas
st.markdown("## Artistas e Frequência de Aparição")

# Contar a quantidade de vezes que cada artista aparece
artist_count = df['Artist'].value_counts().reset_index()
artist_count.index = range(1, len(artist_count) + 1)
artist_count.columns = ['Artista', 'Quantidade de Aparição']

# Exibir a tabela no dashboard
st.dataframe(artist_count)


# Layout em colunas
col1, col2 = st.columns(2)

# Coluna 1: Gráfico de barras
with col1:

    # Converter a coluna 'Release Date' para datetime
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')

    # Criar uma nova coluna 'Year' apenas com o ano
    df['Year'] = df['Release Date'].dt.year

    # Contar a quantidade de músicas por ano
    year_count = df['Year'].value_counts().reset_index()
    year_count.columns = ['Year', 'Count']
    year_count = year_count.sort_values('Year', ascending=False)

    # Gráfico de colunas no Streamlit
    st.markdown("## Lançamentos de Músicas por Ano")
    fig, ax = plt.subplots()
    ax.bar(year_count['Year'], year_count['Count'], color='skyblue')
    ax.set_xlabel("Ano")
    ax.set_ylabel("Quantidade de Músicas")
    ax.set_title("Lançamentos de Músicas por Ano")
    plt.xticks(rotation=45)  # Rotaciona os anos para melhorar a visualização
    st.pyplot(fig)    

with col2:
    year_count_reset = year_count.reset_index(drop=True)
    st.dataframe(year_count_reset[['Year', 'Count']])
