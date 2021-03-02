import os, fnmatch

anno = '2020'
tipo = 'LST_D'

raster_root = os.path.join(r'\\nas-covepi2\gis2\dati_GIS\dati_Italia\dati_satellitari\MODIS\MOD11A2\\'+tipo, 'IT_LONGLAT')  # lettura dati da NAS-COVEPI2

image_folders = [os.path.join(raster_root, dir) for dir in os.listdir(raster_root) if os.path.isdir(os.path.join(raster_root, dir))]

images = []
for image_folder in image_folders:
    if anno in image_folder:
        print(image_folder)
        for root, dirs, files in os.walk(image_folder):
            for name in files:
                if 'FILLED' in name:
                    print(os.path.join(image_folder+'\\', name))
                    images.append(os.path.join(image_folder+'\\', name))

print(len(images))


    