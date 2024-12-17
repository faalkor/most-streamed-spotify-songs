import streamlit as st
import folium
import json
import pandas as pd
import chardet
import os
from graph import graph, aroundStreamings, artistCount, songsYearRelease
import matplotlib.pyplot as plt


# Header
st.markdown("<h1 style='text-align: center;'>Músicas mais tocadas (2024)</h1>", unsafe_allow_html=True)



# Dataset encoding detect
dataset = os.path.join(os.getcwd(), 'app', 'mostStreamedSpotifySongs2024.csv')
with open(dataset, 'rb') as f:
    result = chardet.detect(f.read())


# Ler dataset
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
artistCount(df)

st.markdown("## Lançamentos de Músicas por Ano")
songsYearRelease(df)
