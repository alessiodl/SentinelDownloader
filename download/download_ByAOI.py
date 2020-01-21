# Import
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import os
from config import credentials

# Aree di interesse
geojson = read_geojson('aoi_example.geojson')

anno    = '2018'
mese    = '05'
days    = ['01','31']

# Directory di download
sentinel_dir = r'\\izsfs\dati-gis\SENTINEL2'
img_dir      = anno+'_'+mese
download_dir = os.path.join(sentinel_dir,img_dir)

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Date Strings
fromDate = str(anno+mese+days[0])
toDate   = str(anno+mese+days[1])

# Connessione alle API
copernicusHubAuth = credentials()
username = copernicusHubAuth[0]
password = copernicusHubAuth[1]
api = SentinelAPI( username, password )

# Connect to the API
api = SentinelAPI( username, password, "https://scihub.copernicus.eu/dhus" )

# Individua i singoli poligoni all'interno del file GeoJSON, li converte in WKT e li aggunge alla footprintList
footprintList = []
for i in geojson['features']:
	polygon = geojson_to_wkt(i['geometry'])
	footprintList.append(polygon)

# Esegue la query sulle API Copernicus per ogni poligono della footprintList
productList = []
for fp in footprintList:
	print(fp)
	# Query
	products=api.query(fp,
			date=(fromDate, toDate),
			platformname='Sentinel-2',
			producttype='S2MSI2A')
	# Salva i product ID nella productList			
	for product in products:
		productList.append(product)

if len(products) > 0:
	print("Prodotti trovati: "+str(len(products))+"\n")
	for p in products:
		print("Prod ID: "+p)

	print ("\n"+"INIZIO DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	api.download_all(products,download_dir)
	print ("\n"+"FINE DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("NON CI SONO IMMAGINI DA SCARICARE")