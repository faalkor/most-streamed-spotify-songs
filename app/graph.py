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
    streamings = ['Spotify Streams', 'YouTube Views', 'TikTok Posts', 'Apple Music Playlist Count', 'AirPlay Spins']
    
    # Quantidade de músicas por streaming
    df = pd.DataFrame({"Streaming": streamings})
    count = df["Streaming"].value_counts()

    count.plot(kind="bar", color="skyblue", title="Quantidade de acessos por streaming")
    plt.xlabel("Streaming")
    plt.ylabel("Quantidade")
    plt.show()

    
    # Stats of number 1 song
    # top_data = data.sort_values('Spotify Streams', ascending=False)

    # values = pd.to_numeric(top_data[streamings].iloc[0].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # fig, ax = plt.subplots()
    # ax.pie(values, labels=streamings, autopct='%1.1f%%', startangle=90)
    # ax.axis('equal') 

    # st.pyplot(fig)
