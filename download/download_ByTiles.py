# Import
from collections import OrderedDict
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import os
from config import credentials

regione = 'Puglia'
anno    = '2018'
mese    = '04'
days    = ['01','30']

# Directory di download
sentinel_dir = r'\\izsfs\dati-gis\SENTINEL2'
img_dir      = os.path.join(regione,anno+'_'+mese)
download_dir = os.path.join(sentinel_dir,img_dir)

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Date Strings
fromDate = str(anno+mese+days[0])
toDate   = str(anno+mese+days[1])

# Tiles da scaricare
if regione == 'Abruzzo':
    # Lista Tiles Abruzzo
    tiles = [ '33TUH', '33TVH', '33TUG', '33TVG' ]
elif regione == 'Sardegna':
    # Lista Tiles Sardegna
    tiles = [ '32TML', '32TNL', '32TMK', '33TNK', '32SMJ', '32SNJ' ]
elif regione == 'Puglia':
    # Lista Tiles Puglia
    tiles = [ '33TWE', '33TWF', '33TXE', '33TXF', '33TYE', '33TYF' ]

# Connessione alle API
copernicusHubAuth = credentials()
username = copernicusHubAuth[0]
password = copernicusHubAuth[1]
api = SentinelAPI( username, password )

# Query arguments
query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI2A',
        'date': (fromDate, toDate)
	}

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
		print(p)

	print ("\n"+"INIZIO DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	api.download_all(products, download_dir, max_attempts=3)
	print ("\n"+"FINE DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("NON CI SONO IMMAGINI DA SCARICARE")
