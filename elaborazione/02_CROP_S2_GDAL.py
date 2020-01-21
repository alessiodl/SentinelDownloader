'''
Titolo: CROP_S2_GDAL.py
Autore: Alessio Di Lorenzo
Update: 30/07/2019
Descrizione:
    Dato uno shapefile di punti ed una immagine raster, la procedura:
        - riproietta i dati vettoriali nella proiezione del raster
        - ricava il footprint dell'immagine raster
        - crea il buffer dei punti e l'envelope del buffer
        - seleziona solo gli envelope che si sovrappongono all'impronta (footprint) dell'immagine raster
        - ritaglia il raster con gli envelope selezionati
		- smista i crop all'interno di sottocartelle con il nome della regione riportato nell'attributo 'REGIONE'
'''
import rasterio
from osgeo import gdal
from shapely.geometry import box, shape
from rasterio.plot import show
import geopandas as gpd
import os, fnmatch
import json
from datetime import date, datetime

# regione = 'Toscana'
anno = '2019'
punti_wgs84 = gpd.read_file(r'\\izsfs\dati-gis\SENTINEL2_PUNTI\aziende_2019.shp')
raggio_metri = 2240
# raggio_metri = 5000

#raster_data = os.path.join(r'D:\SENTINEL2_20M_ESTRATTE', anno) # lettura dati estratti dal disco locale
raster_data = os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_ESTRATTE',anno) # lettura dati estratti da SAN
# cropped_dir = os.path.join(os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_CROPPED',anno), regione)
cropped_dir = os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_CROPPED',anno)

# Crea directory di lavoro se non esiste
if not os.path.exists(cropped_dir):
	os.makedirs(cropped_dir)

print("Inizio crop: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
	buffer_gs = punti_utm.buffer(raggio_metri)
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
		regione = i['properties']['REGIONE']
		# Clip del raster usando GDAL Translate e il BBOX del poligono di envelope
		geom_bbox = [b for b in shape(geom).bounds]
		minX = geom_bbox[0]
		minY = geom_bbox[1]
		maxX = geom_bbox[2]
		maxY = geom_bbox[3]
		# Nome del file di output
		cropped_name = raster.name[-34:-4]+"_"+str(cod_azi)
		cropped_name = cropped_name.replace("_20m","")
		# Crea path del file di output se non esiste
		cropped_path = os.path.join(cropped_dir,regione)
		if not os.path.exists(cropped_path):
			os.makedirs(cropped_path)
		cropped_image = os.path.join(cropped_path, cropped_name+".png") 
		# Translate
		gdal.Translate(cropped_image, raster.name, format="PNG", projWin = [minX, maxY, maxX, minY])

print("Fine crop: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))