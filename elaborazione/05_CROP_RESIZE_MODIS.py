import rasterio
from osgeo import gdal
from shapely.geometry import box, shape
from rasterio.plot import show
import geopandas as gpd
import os, fnmatch
import json
from datetime import date, datetime

anno = '2019'
punti_wgs84 = gpd.read_file(r'\\izsfs\dati-gis\SENTINEL2_PUNTI\zanzare_2020.shp')
raggio_metri = 2240

raster_root = r'\\nas-covepi2\gis2\dati_GIS\dati_Italia\dati_satellitari\MODIS\MOD11A2'  # lettura dati da NAS-COVEPI2
# raster_root = os.path.join(r'C:\Users\a.dilorenzo\Desktop\MODIS_TEST')  # lettura dati da NAS-COVEPI2
cropped_dir = os.path.join(r'C:\Users\a.dilorenzo\Desktop\MODIS_TEST\out', anno)

# Crea directory di lavoro se non esiste
if not os.path.exists(cropped_dir):
	os.makedirs(cropped_dir)

print("Inizio crop: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

image_folders = [os.path.join(raster_root, dir) for dir in os.listdir(raster_root) if os.path.isdir(os.path.join(raster_root, dir))]

images = []
for image_folder in image_folders:
	for root, dirs, files in os.walk(os.path.join(image_folder, anno)):
		for name in files:
			if name.startswith('Trasformed'):
				print(os.path.join(image_folder+'\\'+anno, name))
				images.append(os.path.join(image_folder+'\\'+anno, name))

# print(images)

# Ritaglio delle immagini
# pylint: disable=maybe-no-member
for image in images:
	raster = rasterio.open(image,driver='GTiff')
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
	# punti_utm_envelope.to_file(os.path.join(r'C:\Users\a.dilorenzo\Desktop',"envelopes.geojson"), driver='GeoJSON')
	# Envelope compresi interamente nel footprint
	within = punti_utm_envelope[punti_utm_envelope.within(footprint_gdf.geometry[0])]
	# Ritaglio
	geometries = json.loads(within.to_json())
	# print(within)
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
		if "Day" in raster.name:
			cropped_name = raster.name[-39:-20].replace(".","")+"_"+str(cod_azi)
		else:
			cropped_name = raster.name[-41:-20].replace(".","")+"_"+str(cod_azi)
		# Crea path del file di output se non esiste
		cropped_path = os.path.join(cropped_dir,regione)
		if not os.path.exists(cropped_path):
			os.makedirs(cropped_path)
		cropped_image = os.path.join(cropped_path, cropped_name+".tif") 
		# Warp
		gdal.Warp(cropped_image, raster.name, format="GTiff", outputBounds=[minX, minY, maxX, maxY], xRes=20, yRes=20)
		
print("Fine crop: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))