# Import librerie
from collections import OrderedDict
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
from calendar import monthrange
import os
from schema import selectImages
from config import credentials

copernicusHubAuth = credentials()
username = copernicusHubAuth[0]
password = copernicusHubAuth[1]

# Connessione alle API
api = SentinelAPI(username, password)

# Parametri di ricerca variabili
platform = 'Sentinel-2'
product = 'S2MSI2A' #'S2MSI2A' (mesi da 03 a 12 del 2018) o 'S2MSI2Ap' (mesi 01, 02, 03 del 2018)
regione = 'Puglia'
anno = '2019'
# Parametri di ricerca derivati
# fromDate = date(int(anno), int(mese),1).strftime('%Y%m%d')
# toDate = date(int(anno), int(mese), monthrange(int(anno), int(mese))[1]).strftime('%Y%m%d')
tiles = selectImages(regione)

# Directory di download
sentinel_dir = os.path.join(r'\\izsfs\dati-gis\SENTINEL2',anno)
# img_dir = os.path.join(regione, anno+'_'+mese)
download_dir = os.path.join(sentinel_dir, regione)

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Query arguments
query_kwargs = {
    'platformname': platform,
    'producttype': product,
    'date': ('20190630', '20191001') #luglio/agosto/settembre
	#'date': ('20180101', '20190101')
}

# Ricerca immagini per ogni tile
products = OrderedDict()
for tile in tiles:
	kw = query_kwargs.copy()
	kw['filename'] = '*_{}_*'.format(tile)
	pp = api.query(**kw)
	products.update(pp)

# Download
if len(products) > 0:
	size = api.get_products_size(products)
	print("Immagini trovate: {0}".format(len(products)))
	print("Dimensioni complessive download: {0} GB".format(size))
	uuids = [uuid for uuid, prod in products.items()]
	print("\n"+"lista UUID:")
	print(uuids)
	print("\n"+"Inizio download: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	api.download_all(products, download_dir, max_attempts=5)
	print ("Verifica errori di download e recupero: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	for uuid in uuids:
		api.download(uuid, download_dir, checksum=True)
	print ("Fine download: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("Nessuna immagine da scaricare")