import os
import shutil
import sys
from datetime import date, datetime

regione = 'Calabria'
anno = '2019'
# ARCHIVIO IMMAGINI ESTRATTE (SU SAN)
archivio_ex = os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_ESTRATTE',anno)
archivio_ex_reg = os.path.join(archivio_ex, regione)
# ESTRAZIONE DISCO LOCALE (molto più veloce. E' necessario copiare poi a mano su SAN)
extraction_dir = os.path.join(r'D:\SENTINEL2_20M_ESTRATTE',anno)
# DIRECTORY DI LAVORO
working_dir = os.path.join(extraction_dir, regione)

# print("Inizio spostamento dei SAFE dalla cartella di lavoro all'archivio degli estratti: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
for safe_folder in os.listdir(working_dir):
	if not os.path.exists(os.path.join(archivio_ex_reg, safe_folder)):
		if sys.platform == 'win32':
			print("Spostamento di "+safe_folder)
			os.system('xcopy "%s" "%s"' % (os.path.join(working_dir,safe_folder),os.path.join(archivio_ex_reg, safe_folder)))
# print("Fine spostamento: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))