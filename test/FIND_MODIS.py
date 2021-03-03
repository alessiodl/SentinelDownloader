import os, fnmatch
import json

anno = '2019'

raster_root = r'\\nas-covepi2\gis2\dati_GIS\dati_Italia\dati_satellitari\MODIS\MOD11A2'  # lettura dati da NAS-COVEPI2

image_folders = [os.path.join(raster_root, dir) for dir in os.listdir(raster_root) if os.path.isdir(os.path.join(raster_root, dir))]

images = []
for image_folder in image_folders:
	for root, dirs, files in os.walk(os.path.join(image_folder, anno)):
		for name in files:
			if name.startswith('Trasformed'):
				print(os.path.join(image_folder+'\\'+anno, name))
				images.append(os.path.join(image_folder+'\\'+anno, name))

# print(images)