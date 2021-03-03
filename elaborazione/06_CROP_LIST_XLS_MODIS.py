import os
import fnmatch
import datetime
import openpyxl
import pandas as pd

import os
import fnmatch
import datetime
import openpyxl
import pandas as pd

regione = 'MOLISE'
anno = '2019'
cropped_dir = os.path.join(os.path.join(
    r'C:\Users\a.dilorenzo\Desktop\MODIS_TEST\out', anno), regione)

rowTitles = ['NOME_FILE', 'REGIONE', 'PRODOTTO', 'ANNO',
    'MESE', 'GIORNO', 'AZIENDA', 'IMMAGINE', 'DATA']
df = pd.DataFrame(columns=rowTitles)

images = []
for root, dirs, files in os.walk(cropped_dir):
	for name in files:
		if name.endswith(".tif"):
			nome_file = name
			regione = regione.upper()
			product = 'MOD11A2 - '+name[3:-21]
			mese = name[10:12]
			giorno = name[12:14]
			azienda = name[-11:-4]
			immagine = name.replace(".tif", "")
			data = giorno+"/"+mese+"/"+anno

			# print("{},{},{},{},{},{},{},{},{}".format(nome_file, regione, product, anno, mese, giorno, azienda, immagine, data))

			df = df.append({'NOME_FILE':nome_file, 'REGIONE': regione,'PRODOTTO':product,
			'ANNO':anno,'MESE':mese,'GIORNO':giorno,'AZIENDA':azienda,'IMMAGINE':immagine,'DATA':data}, ignore_index=True)

print(df.head(10))
print("Generazione file xlsx...")
df.to_excel(r'C:\Users\a.dilorenzo\Desktop\MODIS_TEST\out\\'+anno+'\lista_immagini_'+regione+'_'+anno+'.xlsx',sheet_name='DATASET_IMMAGINI')
print("File pronto: lista_immagini_"+regione+"_"+anno+".xlsx")
