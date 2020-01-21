import os
import fnmatch
import datetime
import openpyxl
import pandas as pd

archivio_s2 = r'\\izsfs\dati-gis\SENTINEL2'
mydate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

rowTitles = ['regione','immagine','satellite','anno','mese','giorno','ora','orbita','tile']
df = pd.DataFrame(columns=rowTitles)

images = []
for root, dirs, files in os.walk(archivio_s2):
    for name in files:
        regione = root[27:]
        img = name.replace(".zip","")
        satellite = name[0:3]
        anno = name[11:15]
        mese = name[15:17]
        giorno = name[17:19]
        ora = name[19:26]
        orbita = name[33:37]
        tile = name[38:44]
        #print("{},{},{},{},{},{},{},{},{}".format(regione, img, satellite, anno, mese, giorno, ora, orbita,tile))

        df = df.append({'regione': regione,'immagine':img,
                        'satellite':satellite,'anno':anno,
                        'mese':mese,'giorno':giorno,'ora':ora,
                        'orbita':orbita,'tile':tile}, ignore_index=True)

print(df.head(10))
df.to_excel(r'\\izsfs\dati-gis\sentinel2_summary.xlsx',sheet_name='Elenco immagini')