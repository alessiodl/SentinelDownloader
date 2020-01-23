from osgeo import gdal, gdal_array

inputImage  = r'C:\Users\a.dilorenzo\Desktop\T33TUG_20180101T100409_B02_006AQ354.png'
outputImage = r'C:\Users\a.dilorenzo\Desktop\T33TUG_20180101T100409_B02_006AQ354_NORM.tiff'
# Dataset
ds = gdal.Open(inputImage)
# Banda
band = ds.GetRasterBand(1)
# Trasformazione in array
arr = band.ReadAsArray().astype('f4')
# print(arr)
# Apply equation
data = arr/10000
# Save array, using ds as a prototype
gdal_array.SaveArray(data.astype("float32"), outputImage, "GTIFF", ds)

ds = None

