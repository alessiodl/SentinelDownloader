import os
import fnmatch
import datetime
import openpyxl
import pandas as pd

anno = '2021'
cropped_dir = os.path.join(r'\\izsfs\dati-gis\SENTINEL2_20M_CROPPED', anno)

if os.path.isfile(os.path.join(cropped_dir, 'tot_'+anno+'.xlsx')):
	os.remove(os.path.join(cropped_dir, 'tot_'+anno+'.xlsx'))

df = pd.DataFrame()

for root, dirs, files in os.walk(cropped_dir):
	for name in files:
		if name.endswith('.xlsx'):
			print(os.path.join(cropped_dir, name))
			xls_file = os.path.join(cropped_dir, name)
			df = df.append(pd.read_excel(xls_file), ignore_index=True)
			# print(df)

# print(df.head(5))

df.drop(columns=['Unnamed: 0'], inplace=True)
df.to_excel(os.path.join(cropped_dir, 'tot_'+anno+'.xlsx'), sheet_name='DATASET_IMMAGINI', index='False')

