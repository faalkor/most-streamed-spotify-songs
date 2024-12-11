import streamlit as st
import folium
import json
import pandas as pd
import chardet
from graph import graph


# Header
st.markdown("# Músicas mais tocadas no Spotify (2024)")


# Map
with open('app\countrys.json') as f:
    countrysJson = json.load(f)
    m = folium.Map(location=[20, 0], zoom_start=2)
    folium.GeoJson(
        countrysJson
        # ,style_function=lambda x: {
        #     'fillColor': 'green',
        #     'fillOpacity': 1
        # }
        # if x['properties']['name'] == 'Brazil' else{}
    ).add_to(m)
    
    st.components.v1.html(m._repr_html_(), height=450)


# Dataset encoding detect
dataset = 'mostStreamedSpotifySongs2024.csv'

with open(dataset, 'rb') as f:
    result = chardet.detect(f.read())


# Table
st.markdown("## Dados")
df = pd.read_csv(dataset, encoding=result['encoding'])
st.write(df)


# Graphs
st.markdown("### Popularidade por streaming")
graph(df)
