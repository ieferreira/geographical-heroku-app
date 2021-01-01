from pyproj import Transformer
import numpy as np
import folium

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

def makeWGS(lat1,lon1, code1):
    """ 
    Main Process: pyproj coordinate transformation to WGS epsg:4326 (Transformer)
    Input: lat1, lon1 => lists with coordintates to be transformed (list of floats)
            code1 =>  input coordinates epsg code
    Output: coordenadas4326 =>  output coordinates in desired epsg 4326 in list of tuples [(lat, lon), (lat,lon)...]
    """
    transformer = Transformer.from_crs(code1,4326) 
    lats = list(map(float, lat1.split(',')))
    lons = list(map(float, lon1.split(',')))
    puntos = list(zip(lats, lons))
    coordenadas4326 = []
    for pt in transformer.itransform(puntos):
        coordenadas4326.append(((round(pt[0], 2)), round(pt[1], 2)))
    return coordenadas4326    

def centroid(arr):
    """
    Main Process: mean of coordinates in x and y
    Input: Array of coordinates
    Output: Centroid of the coordinates
    """
    arr = np.array(arr)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return (sum_x/length, sum_y/length)

def mapit(puntos, center):
    """
    Main Process: map points on folium map object
    Input: Array of coordinates
    Output: folium map object
    """
    map = folium.Map(location=center, zoom_start=7)
    for point in range(len(puntos)):
        folium.Marker(puntos[point]).add_to(map)    
    return map    