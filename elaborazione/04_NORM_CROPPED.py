from osgeo import gdal, gdal_array

inputImage  = r'C:\Users\a.dilorenzo\Desktop\T33TUG_20190101T100411_B02_006AQ354.png'
outputImage = r'C:\Users\a.dilorenzo\Desktop\T33TUG_20190101T100411_B02_006AQ354_NORM.tiff'
# Dataset
ds = gdal.Open(inputImage)
# Band
band = ds.GetRasterBand(1)
# Read as numpy array
arr = band.ReadAsArray().astype('f4')
# print(arr)
# Apply normalization
data = arr/10000 # divide tutti i valori per 10000
data[data > 1] = 1 # imposta a 1 tutti i valori maggiori di 1
# Save array, using ds as a prototype
gdal_array.SaveArray(data.astype("float32"), outputImage, "GTIFF", ds)
# Empty ds variable
ds = None

