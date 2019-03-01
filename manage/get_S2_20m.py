
'''
Titolo: GET_S2_20m.py
Autore: Alessio Di Lorenzo
Update: 01/03/2019
Descrizione:
    Per ogni dato Sentinel 2 in formato zip presente in archivio (NAS):
        1) Copia lo zip sentinel in una cartella di lavoro locale;
        2) Decomprime lo zip in una cartella .SAFE
        3) Pulisce la cartella .SAFE lasciando solo le bande a 20 metri
'''
import zipfile
from datetime import date, datetime
import os, fnmatch
from shutil import copyfile, rmtree

# Parametri
regione = 'Puglia'
anno = '2018'
mese = '01'
archivio_s2 = r'\\izsfs\dati-gis\SENTINEL2'
working_dir = r'C:\Users\a.dilorenzo\Desktop\S2_WD'
# Crea directory di lavoro se non esiste
if not os.path.exists(working_dir):
    os.makedirs(working_dir)

# Percorsi
subarchivio_s2 = os.path.join(regione,anno+'_'+mese)
path_to_zip_files = os.path.join(archivio_s2, subarchivio_s2)

# Lista dei file zip da decomprimere
zipped_files = [f for f in os.listdir(path_to_zip_files)]
print( "[Num. "+str(len(zipped_files))+" file trovati in archivio]" )


for zipped_file in zipped_files:
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
            if fnmatch.fnmatch(name, '*_B*_20m.jp2'):
                copyfile(os.path.join(root,name), os.path.join(safe_dir,name))
            else:
                os.remove(os.path.join(root,name))
    # Rimozione delle cartelle vuote della cartella .SAFE
    # *****************************************************************
    for element in os.listdir(safe_dir):
        if element in ['AUX_DATA','DATASTRIP','GRANULE','HTML','rep_info']:
            rmtree(os.path.join(safe_dir,element))
    # *****************************************************************
    print("Fine: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
