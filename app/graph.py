import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def graph(data):                                                                                           
    # Remove dataset commas and convert to int
    data['Spotify Streams'] = pd.to_numeric(data['Spotify Streams'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # definir colunas
    columns = ['Track', 'Artist','Release Date', 'Spotify Streams', 'YouTube Views',
                'TikTok Views', 'AirPlay Spins', 'Pandora Streams', 'Soundcloud Streams', 'Shazam Counts']

    # total
    num_songs = len(data)

    # sort data
    slider_num = st.slider("Selecione o número de faixas a visualizar:", 1, num_songs, min(10, num_songs))
    top_data = data.sort_values('Spotify Streams', ascending=False).head(slider_num)

    # ranking index
    top_data.reset_index(drop=True, inplace=True)
    top_data.index = range(1, len(top_data) + 1)

    top_data = top_data[columns]    
    
    st.write(top_data)

def aroundStreamings(data):
    # Colunas de interesse
    streamings = ['Spotify Streams', 'YouTube Views', 'TikTok Posts', 'Shazam Counts', 'AirPlay Spins']

    # Verificar se as colunas existem no dataset
    missing_columns = [col for col in streamings if col not in data.columns]
    if missing_columns:
        st.write(f"As seguintes colunas estão ausentes no dataset: {', '.join(missing_columns)}")
        return

    # Função para remover separadores de milhar e lidar com NaN
    def clean_numbers(value):
        if pd.isna(value):  # Verifica se o valor é NaN
            return 0  # Substitui NaN por 0
        if isinstance(value, str):
            return int(value.replace(',', '').replace('.', '').strip())
        return int(value)

    # Limpeza e conversão de dados
    for col in streamings:
        data[col] = data[col].apply(clean_numbers)

    # Somar valores individuais de cada coluna
    totals = {streaming: int(data[streaming].sum()) for streaming in streamings}

    # Exibir os resultados no dashboard
    st.markdown("### Total de Visualizações por Plataforma de Streaming")
    st.write(totals)

    # Criar gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(totals.keys(), totals.values(), color="skyblue")

    # Personalizar o gráfico
    ax.set_title("Comparação de Visualizações por Plataforma")
    ax.set_xlabel("Plataformas")
    ax.set_ylabel("Total de Visualizações (Escala Logarítmica)")

    # Configurar escala logarítmica no eixo y
    ax.set_yscale('log')
    plt.xticks(rotation=45)

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

def artistCount(data):
    artist_count = data['Artist'].value_counts().reset_index()
    artist_count.index = range(1, len(artist_count) + 1)
    artist_count.columns = ['Artista', 'Quantidade de Aparição']

    # Exibir a tabela no dashboard  
    st.dataframe(artist_count)


def songsYearRelease(data):
    # Layout em colunas
    col1, col2 = st.columns(2)

    # Coluna 1: Gráfico de barras
    with col1:
        # Converter a coluna 'Release Date' para datetime
        data['Release Date'] = pd.to_datetime(data['Release Date'], errors='coerce')

        # Criar uma nova coluna 'Year' apenas com o ano
        data['Year'] = data['Release Date'].dt.year

        # Contar a quantidade de músicas por ano
        year_count = data['Year'].value_counts().reset_index()
        year_count.columns = ['Year', 'Count']
        year_count = year_count.sort_values('Year', ascending=False)

        # Gráfico de colunas no Streamlit
        fig, ax = plt.subplots()
        ax.bar(year_count['Year'], year_count['Count'], color='skyblue')
        ax.set_xlabel("Ano")
        ax.set_ylabel("Quantidade de Músicas")
        ax.set_title("Lançamentos de Músicas por Ano")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        year_count_reset = year_count.reset_index(drop=True)
        st.dataframe(year_count_reset[['Year', 'Count']])
