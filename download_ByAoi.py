from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import os

# Aree di interesse
geojson = read_geojson('aoi_example.geojson')

# Directory di download
download_dir = "img"

# Connessione alle API
username = "mySciHubUsername"
password = "mySciHubPassword"
api 	 = SentinelAPI( username, password )

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
			date=('20181219', date(2018, 12, 29)),
			platformname='Sentinel-2',
			producttype='S2MSI2A')
	# Salva i product ID nella productList			
	for product in products:
		productList.append(product)

for p in productList:
	print("Prod ID: "+p)
	#print('\n')
	#print(api.get_product_odata(p, full=False))
					 
# Download
print ("\n"+"INIZIO DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
api.download_all(productList)
print ("\n"+"FINE DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
