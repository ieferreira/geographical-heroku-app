import streamlit as st
from pyproj import Transformer
import pandas as pd 
import folium
from streamlit_folium import folium_static

def geotransform(lat1,lon1, code1, code2):
    """ 
    Main Process: pyproj coordinate transformation (Transformer)
    Input: lat1, lon1 => lists with coordintates to be transformed (list of floats)
            code1 =>  input coordinates epsg code
            code2 =>  desired output epsg code 
    Output: puntos =>  original coordinates in list of tuples [(lat, lon), (lat,lon)...]
            nuevas_coordenadas =>  output coordinates in desired epsg output code (code2) in list of tuples [(lat, lon), (lat,lon)...]
    """
    transformer = Transformer.from_crs(code1,code2) 
    lats = list(map(float, lat1.split(',')))
    lons = list(map(float, lon1.split(',')))
    puntos = list(zip(lats, lons))
    nuevas_coordenadas = []
    for pt in transformer.itransform(puntos):
        nuevas_coordenadas.append(((round(pt[0], 2)), round(pt[1], 2)))
    return puntos, nuevas_coordenadas


st.markdown("""## Coordinate conversion (v0.3)""")
st.markdown("An app to facilitate quick conversion between geographical coordinates")


code1 = st.text_input('Input current EPSG code (E.G WGS is 4326):') 

code2 = st.text_input('Input target EPSG code (E.G MAGNA SIRGAS BOGOTÁ is 3116):') 

if code1 and code2: 
    # checks if user has typed the codes for the transformation
    while True:
        try:
            code1 = int(code1) # users inputs a string
            code2 = int(code2)
            break
        except:
            st.write("Please input valid numbers")
    lat1 = st.text_input('Input latitudes (separated by commas):')
    lon1 = st.text_input('Input longitudes (separated by commas):')   
    if lat1 and lon1:        
        puntos, nuevas_coordenadas = geotransform(lat1, lon1, code1, code2)
        df = pd.DataFrame({"Input Coordinates (lat/lon)": puntos, "Output Coordinates (lat/lon)": nuevas_coordenadas})
        st.write(df)
        for i in range(len(nuevas_coordenadas)):
            if i == 0:
                st.write(f"Input Coordinates <{str(code1)}>", f"Target Coordinates <{str(code2)}>")

        if code1 == 4326:
            map = folium.Map(location=list(puntos[0]))
            for point in range(len(puntos)):
                folium.Marker(puntos[point]).add_to(map)
            #display map
            folium_static(map)
        else: 
            try:
                puntosref, _ = geotransform(lat1, lon1, code1, 4326)
                map = folium.Map(location=list(puntos[0]))
                for point in range(len(puntos)):
                    folium.Marker(puntos[point]).add_to(map)
                #display map
                folium_static(map)
            except:
                st.write("Couldn't display a map, are your epsg codes and coordinates valid?")

st.markdown("Programmed by Iván Ferreira, UnalGeo-Bogotá (2020). [Github! 🎯](https://github.com/ieferreira)")