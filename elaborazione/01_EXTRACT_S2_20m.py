'''
Titolo: EXTRACT_S2_20m.py
Autore: Alessio Di Lorenzo
Update: 31/07/2019
Descrizione:
    Per ogni dato Sentinel 2 in formato zip presente in archivio (SAN):
		1) Verifica che l'immagine non sia già presente nell'archivio dei dati estratti
        2) Copia lo zip sentinel in una cartella di lavoro locale
        3) Decomprime lo zip in una cartella .SAFE
        4) Pulisce la cartella .SAFE lasciando solo le bande a 20 metri
        5) Rinomina le MSK in maniera coerente rispetto alle altre bande, necessario per archivi successivi a Marzo 2018
        6) Rimuove le immagini "VIS", presenti solo per gli archivi precedenti ad Aprile 2018
		7) Sposta la cartella SAFE dalla working_dir all'archivio estratti
'''
import zipfile
from datetime import date, datetime
import os, fnmatch
from shutil import copyfile, rmtree, move

# Parametri
regione = 'Friuli'
anno = '2018'

# ARCHIVIO ZIP SENTINEL2
archivio_s2 = os.path.join(r'\\izsfs\dati-gis\SENTINEL2',anno)
# ARCHIVIO IMMAGINI ESTRATTE (SU SAN)
archivio_ex = os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_ESTRATTE',anno)
archivio_ex_reg = os.path.join(archivio_ex, regione)
# ESTRAZIONE DISCO LOCALE (molto più veloce. E' necessario copiare poi a mano su SAN)
extraction_dir = os.path.join(r'D:\SENTINEL2_20M_ESTRATTE',anno)
# DIRECTORY DI LAVORO
working_dir = os.path.join(extraction_dir, regione)

# Crea directory di lavoro se non esiste
if not os.path.exists(working_dir):
    os.makedirs(working_dir)

path_to_zip_files = os.path.join(archivio_s2, regione)

# Lista dei file zip da decomprimere
zipped_files = [f for f in os.listdir(path_to_zip_files)]
print( "[Num. "+str(len(zipped_files))+" file trovati in archivio]" )

for zipped_file in zipped_files:
	if os.path.exists(os.path.join(archivio_ex_reg, zipped_file.replace(".zip",".SAFE"))):
		# Controlla se esiste la cartella SAFE per l'archivio. Se la trova passa allo zip successivo
		# altrimenti estrae il dato
		print(str(zipped_file)+" è già presente nell'archivio dei dati estratti")
	else:
		print("Inizio: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		# Copia file zippato in locale
		# *****************************************************************
		print("Copia di {0} nella directory di lavoro".format(zipped_file))
		copyfile(os.path.join(path_to_zip_files, zipped_file), os.path.join(working_dir, zipped_file))
		# Estrazione in cartella .SAFE
		# *****************************************************************
		print("Estrazione di {0} nella corrispondente cartella .SAFE".format(zipped_file))
		zip_ref = zipfile.ZipFile(os.path.join(working_dir,zipped_file),'r')
		zip_ref.extractall(working_dir)
		zip_ref.close()
		# Rimozione file zippato dalla cartella di lavoro
		# *****************************************************************
		print("Rimozione dell'archivio zip dalla cartella di lavoro")
		os.remove(os.path.join(working_dir, zipped_file))
		# Rimozione delle informazioni non necessarie dalla cartella .SAFE
		# *****************************************************************
		print("Rimozione dei dati non necessari dalla cartella .SAFE")
		safe_dir = os.path.join(working_dir, zipped_file.replace('.zip','.SAFE'))
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if fnmatch.fnmatch(name, '*_20m.jp2'):
					copyfile(os.path.join(root,name), os.path.join(safe_dir,name))
				else:
					os.remove(os.path.join(root,name))
		# Rimozione delle cartelle vuote della cartella .SAFE
		# *****************************************************************
		for element in os.listdir(safe_dir):
			if element in ['AUX_DATA','DATASTRIP','GRANULE','HTML','rep_info']:
				rmtree(os.path.join(safe_dir,element))
		# *****************************************************************
		print("Modifica del nome delle MSK - necessario per archivi successivi a Marzo 2018")
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if len(name) == 38:
					os.rename(os.path.join(root,name),os.path.join(root,name[4:]))
				if fnmatch.fnmatch(name, '*MSK_*'):
					substring = root[-27:-21]+"_"+root[-54:-39]+"_"
					original_name = os.path.join(root, name)
					renamed_name = os.path.join(root, str(substring)+name.replace("MSK_","").replace("PRB",""))
					os.rename(original_name,renamed_name)
		# *****************************************************************
		print("Rimozione immagini 'VIS', presenti solo per gli archivi precedenti ad Aprile 2018 e aggiunta prefisso 'S2A_' o 'S2B_'")
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if fnmatch.fnmatch(name, '*_VIS_*'):
					# rimuove 'VIS'
					os.remove(os.path.join(root,name))
				else:
					# aggiunge prefisso 'S2A_' o 'S2B_'
					original_name = os.path.join(root, name)
					prefix = os.path.basename(safe_dir)[0:3]
					prefix_name = os.path.join(root, prefix+"_"+name)
					os.rename(original_name, prefix_name)
		# *****************************************************************
		print("Fine: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
		
# Spostamento dei dati estratti dalla cartella di lavoro all'archivio degli estratti (lento... conviene copiare a mano da D a SAN per ora)
'''
print("Inizio spostamento dei SAFE dalla cartella di lavoro all'archivio degli estratti: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
for safe_folder in os.listdir(working_dir):
	if not os.path.exists(os.path.join(archivio_ex_reg, safe_folder)):
		print("Spostamento di "+safe_folder)
		move(os.path.join(working_dir,safe_folder),archivio_ex_reg)
print("Fine spostamento: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
'''