import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def graph(data):                                                                                    # radio stations       
    # Remove dataset commas and convert to int
    data['Spotify Streams'] = pd.to_numeric(data['Spotify Streams'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # total
    num_songs = len(data)

    # sort data
    slider_num = st.slider("Selecione o número de faixas a visualizar:", 1, num_songs, min(10, num_songs))
    top_data = data.sort_values('Spotify Streams', ascending=False).head(slider_num)
    st.write(top_data)


def aroundStreamings(data):
    streamings = ['Spotify Streams', 'YouTube Views', 'TikTok Posts', 'Apple Music Playlist Count', 'AirPlay Spins']
    data['Spotify Streams'] = pd.to_numeric(data['Spotify Streams'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # Stats of number 1 song
    values = pd.to_numeric(top_data[streamings].iloc[0].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    fig, ax = plt.subplots()
    ax.pie(values, labels=streamings, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 


    # Plotagem do graph
    st.pyplot(fig)
