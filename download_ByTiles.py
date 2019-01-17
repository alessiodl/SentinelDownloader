from collections import OrderedDict
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import os

# Lista Tiles Abruzzo
tiles = [ '33TUH', '33TVH', '33TUG', '33TVG' ]
# Directory di download
download_dir = "img"

# Connessione alle API
username = "mySciHubUsername"
password = "mySciHubPassword"
api 	 = SentinelAPI( username, password )

# Query arguments
query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI2A',
        'date': ('20180501', '20180531')}

# Ricerca immagini per ogni tile
products = OrderedDict()
for tile in tiles:
	kw = query_kwargs.copy()
	kw['filename'] = '*_T{}_*'.format(tile)
	pp = api.query(**kw)
	products.update(pp)
					 
# Download
if len(products) > 0:
	print("Prodotti trovati: "+str(len(products))+"\n")
	for p in products:
		print("Prod ID: "+p)
		# print('\n')
		# print(api.get_product_odata(p, full=False))
		
	print ("\n"+"INIZIO DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	api.download_all(products,os.path.join(download_dir,'2018_05'))
	
	print ("\n"+"FINE DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("NON CI SONO IMMAGINI DA SCARICARE")