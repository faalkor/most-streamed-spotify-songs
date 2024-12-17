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
    
    # Ignorar registro com streaming sem dados
    data_clean = data.dropna(subset=streamings)
    
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
