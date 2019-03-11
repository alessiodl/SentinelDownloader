'''
Titolo: CROP_S2.py
Autore: Alessio Di Lorenzo
Update: 11/03/2019
Descrizione:
    Dato il file vettoriale degli envelope delle trappole e il raster da ritagliare:
        1) seleziona gli envelope che si sovrappongono all'impronta (footprint) dell'immagine
'''
import rasterio
from shapely.geometry import box
from rasterio.plot import show
from rasterio.mask import mask
import geopandas as gpd
import os, fnmatch
import json

# Dati di input
raster_data = r'C:\Users\a.dilorenzo\Desktop\S2_WD'
vector_data = r'C:\Users\a.dilorenzo\Desktop\data\trappole_envelopes_25.geojson'

# Directory di output
cropped_dir = r'C:\Users\a.dilorenzo\Desktop\CROPPED'

images = []
for root, dirs, files in os.walk(raster_data):
    for name in files:
        if fnmatch.fnmatch(name, '*_20m.jp2'):
            images.append(os.path.join(root, name))

# Ritaglio delle immagini
for image in images:
    # print(image)
    raster = rasterio.open(image, driver='JP2OpenJPEG')
    # footprint del raster
    l = raster.bounds[0]
    b = raster.bounds[1]
    r = raster.bounds[2]
    t = raster.bounds[3]
    # box(minx, miny, maxx, maxy, ccw=True)
    b = box(l, b, r, t)
    # b.wkt
    # Creazione del geodataframe dal poligono di footprint del raster
    footprint_gdf = gpd.GeoDataFrame(gpd.GeoSeries(b), columns=['geometry'])
    # Assegnazione al GeoDataFrame del SR del raster
    footprint_gdf.crs = raster.crs.data
    # Lettura del file GeoJSON come GeoDataFrame
    vector_gdf = gpd.read_file(vector_data)
    # Riproiezione del GeoDataFrame nel SR del raster
    vector_gdf = vector_gdf.to_crs(raster.crs.data)
    intersections = gpd.overlay(vector_gdf, footprint_gdf, how='intersection')
    # Lettura del file GeoJSON come GeoDataFrame
    gdf = gpd.read_file(vector_data)
    # Riproiezione del GeoDataFrame nel SR del raster
    gdf = gdf.to_crs(raster.crs.data)
    # Geometrie (nel formato accettato dalla funzione mask di rasterio)
    geometries = json.loads(intersections.to_json())
    # Ritaglio
    idx = 0
    for i in geometries['features']:
        idx += 1
        geom = i['geometry']
        # Clip del raster usando il poligono come maschera
        out_image, out_transform = mask(dataset=raster, shapes=[geom], crop=True)
        # Copia dei metadati del dato originale
        out_meta = raster.meta.copy()

        out_meta.update({"driver": "PNG",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        cropped_name = raster.name[-34:-4]+"_crop_"+str(idx)
        cropped_image = os.path.join(cropped_dir, cropped_name+".png")

        with rasterio.open(cropped_image, "w", **out_meta) as dest:
            dest.write(out_image)
