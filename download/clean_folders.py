'''
Rimuove dalle cartelle dell'archivio i file che non rientrano nello schema prefissato di download.
Questa situazione si verifica per i dati scaricati prima della definizione dello schema
'''
import os, fnmatch
from schema import selectImages

regione = 'Sardegna'
# anno = '2018'
tiles = selectImages(regione)
sentinel_dir = r'\\izsfs\dati-gis\SENTINEL2'
working_dir = os.path.join(sentinel_dir, regione)

s2_files = os.listdir(working_dir)
print("immagini nella cartella: {0}".format(len(s2_files)))
print("tiles: {0}".format(tiles))

valide = []
for tile in tiles:
    for image in s2_files:
        if fnmatch.fnmatch(image, '*_'+tile+"_*"):
            valide.append(image)

print("immagini valide: {0}".format(len(valide)))

non_valide = []
for image in s2_files:
    if image not in valide:
        non_valide.append(image)

print("immagini non valide: {0}".format(len(non_valide)))

# Pulizia
'''
for image in non_valide:
    os.remove(os.path.join(working_dir, image))
'''