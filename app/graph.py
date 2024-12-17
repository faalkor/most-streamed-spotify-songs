import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    streamings = ['Spotify Streams', 'YouTube Views', 'TikTok Posts', 'Shazam Counts', 'AirPlay Spins']

    # Verificar se os streamings existem no dataset
    if not set(streamings).issubset(data.columns):
        st.write(f"Algumas colunas não existem no dataset: {set(streamings) - set(data.columns)}")
        return

    # Exibir os primeiros dados nas colunas de streaming para entender o que há nos dados
    st.write("Exibição das primeiras linhas de dados nas colunas de streaming antes da conversão:")
    st.write(data[streamings])

    # Converte para numérico e ignora registros com dados ausentes
    data[streamings] = data[streamings].apply(pd.to_numeric, errors='coerce')

    # Verifica se há NaN após a conversão
    st.write("Após conversão para numérico, valores ausentes (NaN) nas colunas de streaming:")
    st.write(data[streamings].isna().sum())

    # Substitui NaN por 0 (ou outro valor desejado)
    data[streamings] = data[streamings].fillna(0)

    # Agora converte para int64
    data[streamings] = data[streamings].astype('int64')

    # Verificar tipos após a conversão
    st.write("Tipos de dados nas colunas após conversão para int64:")
    st.write(data[streamings].dtypes)

    # Remover registros com NaN
    data_clean = data.dropna(subset=streamings)

    # Verificar se o dataset ficou vazio após o drop
    if data_clean.empty:
        st.write("Nenhum dado válido após a remoção dos valores ausentes nas colunas de streaming.")
    else:
        st.write("Dataset após a limpeza de dados ausentes:")
        st.write(data_clean)


    # Caso não haja dados após o drop, verificar o motivo
    if data_clean.empty:
        st.write("Nenhum dado válido após a remoção dos valores ausentes nas colunas de streaming.")

    # Quantidade de músicas por streaming
    for streaming in streamings:
        data_clean[streaming] = pd.to_numeric(data_clean[streaming], errors='coerce').fillna(0)

    count = {streaming: data_clean[streaming].sum() for streaming in streamings}
    st.write(count)

    fig, ax = plt.subplots()
    ax.bar(count.keys(), count.values(), color="skyblue")
    ax.set_title("Quantidade de acessos por streaming")
    ax.set_xlabel("Streaming")
    ax.set_ylabel("Quantidade")
    plt.xticks(rotation=45)

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
