'''
Titolo: CROP_LIST_XLS.py
Autore: Alessio Di Lorenzo
Update: 29/07/2019
Descrizione:
	esporta un file excel con l'elenco dei crop
'''
import os
import fnmatch
import datetime
import openpyxl
import pandas as pd

regione = 'TOSCANA'
anno = '2019'
cropped_dir = os.path.join(os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_CROPPED',anno), regione)

rowTitles = ['NOME_FILE','REGIONE','TILE','ANNO','MESE','GIORNO','ORA','BANDA','AZIENDA','IMMAGINE','DATA']
df = pd.DataFrame(columns=rowTitles)

images = []
for root, dirs, files in os.walk(cropped_dir):
	for name in files:
		if name.endswith(".png"):
			nome_file = name
			regione = regione.upper()
			tile = name[0:6]
			anno = name[7:11]
			mese = name[11:13]
			giorno = name[13:15]
			ora = name[15:22]
			banda = name[23:26]
			azienda = name[27:35]
			immagine = name.replace(".png","")
			data = giorno+"/"+mese+"/"+anno

			#print("{},{},{},{},{},{},{},{},{}".format(regione, img, satellite, anno, mese, giorno, ora, orbita,tile))

			df = df.append({'NOME_FILE':nome_file,'REGIONE': regione,'TILE':tile,
							'ANNO':anno,'MESE':mese,'GIORNO':giorno,'ORA':ora,
							'BANDA':banda,'AZIENDA':azienda,'IMMAGINE':immagine,'DATA':data},ignore_index=True)

print(df.head(10))
print("Generazione file xlsx...")
df.to_excel(r'\\izsfs\dati-gis\SENTINEL2_20M_CROPPED\\'+anno+'\lista_immagini_'+regione+'_'+anno+'.xlsx',sheet_name='DATASET_IMMAGINI')
print("File pronto: lista_immagini_"+regione+"_"+anno+".xlsx")