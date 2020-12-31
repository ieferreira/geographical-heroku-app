import streamlit as st
from pyproj import Transformer
import numpy as np 
import pandas as pd 

st.markdown("""## Coordinate conversion""")
st.markdown("An app to facilitate quick conversion between geographical coordinates")


code1 = st.text_input('Input current EPSG code (E.G WGS is 4326):') 

code2 = st.text_input('Input target EPSG code (E.G MAGNA SIRGAS BOGOTÁ is 3116):') 

if code1 and code2: 
    code1 = int(code1)
    code2 = int(code2)

    transformer = Transformer.from_crs(code1,code2) # in, out

    lat1 = st.text_input('Input latitudes:')
    lon1 = st.text_input('Input longitudes:') 


    nuevas_coordenadas = []
    if lat1 and lon1:
        lats = list(map(float, lat1.split(',')))
        lons = list(map(float, lon1.split(',')))
        puntos = list(zip(lats, lons))
        # for i in transformer.itransform(puntos):
        #     nuevas_coordenadas.append(i)
        for pt in transformer.itransform(puntos):
            nuevas_coordenadas.append(pt)

        df = pd.DataFrame({"Input Coordinates (lat/lon)": puntos, "Output Coordinates (lat/lon)": nuevas_coordenadas})
        st.write(df)



        for i in range(len(nuevas_coordenadas)):
            if i == 0:
                st.write(f"Input Coordinates <{str(code1)}>", f"Target Coordinates <{str(code2)}>")
            #st.write(puntos[i],"\t\t", nuevas_coordenadas[i])


    st.markdown("Programado por Iván Ferreira, UnalGeo-Bogotá (2020). [Github! 🎯](https://github.com/ieferreira)")