# Import
from collections import OrderedDict
from sentinelsat import SentinelAPI
import os

# Connessione alle API
username = "mySciHubUsername"
password = "mySciHubPassword"
api 	   = SentinelAPI( username, password )

# Riferimenti file
archivio = r'D:\archivio\S2DATA'
mese = '2018_02'
imgPath = os.path.join(archivio,mese)
imgFiles = os.listdir(imgPath)

productFilesPath = [ os.path.join(imgPath,file) for file in imgFiles ]
responseDict = api.check_files(productFilesPath)
# Popola una lista con gli id dei download corrotti da riscaricare
IDs = [ value[0]['id'] for key,value in responseDict.items() ]
print(IDs)

# Directory di download
download_dir = os.path.join(archivio,mese)
# Download
if len(IDs) > 0:
	print("Prodotti corrotti da riscaricare: "+str(len(products))+"\n")
	for p in IDs:
		print("Prod ID: "+p)

	print ("\n"+"INIZIO DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	api.download_all(products,download_dir)
	print ("\n"+"FINE DOWNLOAD: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("NON CI SONO IMMAGINI CORROTTE DA RISCARICARE")
