'''
Titolo: CROP_S2.py
Autore: Alessio Di Lorenzo
Update: 11/03/2019
Descrizione:
    Dato uno shapefile di punti ed una immagine raster, la procedura:
        - riproietta i dati vettoriali nella proiezione del raster
        - ricava il footprint dell'immagine raster
        - riproietta i dati vettoriali nella proiezione del raster
        - crea il buffer dei punti e l'envelope del buffer
        - seleziona solo gli envelope che si sovrappongono all'impronta (footprint) dell'immagine raster
        - ritaglia il raster con gli envelope selezionati
'''
import rasterio
from osgeo import gdal
from shapely.geometry import box, shape
from rasterio.plot import show
import geopandas as gpd
import os, fnmatch
import json

# Dati di input
raster_data = r'D:\S2_WD'
punti_wgs84 = gpd.read_file(r'D:\Python_scripts\SENTINEL\elaborazione\vector_input\punti_prova.shp')
# Directory di output
cropped_dir = r'C:\Users\a.dilorenzo\Desktop\CROPPED'

images = []
for root, dirs, files in os.walk(raster_data):
    for name in files:
        images.append(os.path.join(root, name))

# Ritaglio delle immagini
# pylint: disable=maybe-no-member
for image in images:
    print(image)
    raster = rasterio.open(image, driver='JP2OpenJPEG')
    # footprint del raster
    l = raster.bounds[0]
    b = raster.bounds[1]
    r = raster.bounds[2]
    t = raster.bounds[3]
    # box(minx, miny, maxx, maxy, ccw=True)
    b = box(l,b,r,t)
    # Creazione del geodataframe dal poligono di footprint del raster
    footprint_gdf = gpd.GeoDataFrame(gpd.GeoSeries(b), columns=['geometry'])
    # Riproiezione punti input
    punti_utm = punti_wgs84.to_crs(raster.crs.data)
    # Buffer dei punti proiettati
    buffer_gs = punti_utm.buffer(5000)
    buffer_gdf = gpd.GeoDataFrame({'buffer_geom':buffer_gs}, geometry='buffer_geom')
    # Crea GeoSeries calcolando gli envelope del buffer
    envelope_gs = gpd.GeoSeries(buffer_gdf['buffer_geom'].envelope)
    # Aggiunta la colonna con la geometria degli envelope al geodaframe dei punti
    punti_utm['envelope_geometry'] = envelope_gs
    # Rimozione della geometria dei punti
    punti_utm.drop('geometry', axis=1, inplace=True)
    # Crea nuovo geodataframe con gli envelope
    punti_utm_envelope = gpd.GeoDataFrame(punti_utm, geometry='envelope_geometry')
    punti_utm_envelope.crs = raster.crs.data
    # Trova gli envelope compresi interamente nel footprint
    # Envelope compresi interamente nel footprint
    within = punti_utm_envelope[punti_utm_envelope.within(footprint_gdf.geometry[0])]
    # Ritaglio
    geometries = json.loads(within.to_json())
    for i in geometries['features']:
        geom = i['geometry']
        cod_azi = i['properties']['COD_AZIEND']
        # Clip del raster usando GDAL Translate e il BBOX del poligono di envelope
        geom_bbox = [b for b in shape(geom).bounds]
        minX = geom_bbox[0]
        minY = geom_bbox[1]
        maxX = geom_bbox[2]
        maxY = geom_bbox[3]
        # Nome del file di output
        cropped_name = raster.name[-34:-4]+"_AZI_"+str(cod_azi)
        cropped_name = cropped_name.replace("_20m","")
        cropped_image = os.path.join(r"C:\Users\a.dilorenzo\Desktop\CROPPED_TEST",cropped_name+".png") 
        # Translate
        gdal.Translate(cropped_image, raster.name, format="PNG", projWin = [minX, maxY, maxX, minY])