import streamlit as st
import pandas as pd 
import folium
from helper import *
from streamlit_folium import folium_static



# loads a css style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.markdown("""## Coordinate conversion (v0.4)""")
st.markdown("An app to facilitate quick conversion between geographical coordinates")


code1 = st.text_input('Input current EPSG code (E.G WGS is 4326):') 

code2 = st.text_input('Input target EPSG code (E.G MAGNA SIRGAS BOGOTÁ is 3116):') 

#* checks if user has typed the codes for the transformation
if code1 and code2:     
    while True:
        try:
            code1 = int(code1) #* users inputs a string convert to int
            code2 = int(code2)
            break
        except:
            st.write("Please input valid numbers")
    lat1 = st.text_input('Input latitudes (separated by commas):')
    lon1 = st.text_input('Input longitudes (separated by commas):')   
    if lat1 and lon1:        
        puntos_org, nuevas_coordenadas = geotransform(lat1, lon1, code1, code2)
        puntos = puntos_org
        if code1 != 4326: 
            coordwgs = makeWGS(lat1, lon1, code1)
            puntos = coordwgs
        center = centroid(puntos)
        df = pd.DataFrame({"Input Coordinates (lat/lon)": puntos_org, "Output Coordinates (lat/lon)": nuevas_coordenadas})
        st.write(df)
        for i in range(len(nuevas_coordenadas)):
            if i == 0:
                st.write(f"Input Coordinates <{str(code1)}>", f"Target Coordinates <{str(code2)}>")
        map = mapit(puntos, center)
        folium_static(map)

st.markdown("Programmed by Iván Ferreira, UnalGeo-Bogotá (2020). [Github! 🎯](https://github.com/ieferreira)")