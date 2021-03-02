import rasterio
from osgeo import gdal
from shapely.geometry import box, shape
from rasterio.plot import show
import geopandas as gpd
import os, fnmatch
import json
from datetime import date, datetime

punti_wgs84 = gpd.read_file(r'\\izsfs\dati-gis\SENTINEL2_PUNTI\zanzare_2020.shp')

image = r'\\izsfs\dati-gis\SENTINEL2_20M_ESTRATTE\2019\Abruzzo\S2A_MSIL2A_20190101T100411_N0211_R122_T33TUH_20190101T112837.SAFE\S2A_T33TUH_20190101T100411_B8A_20m.jp2'



raster = rasterio.open(image, driver='JP2OpenJPEG')
# footprint del raster
l = raster.bounds[0]
b = raster.bounds[1]
r = raster.bounds[2]
t = raster.bounds[3]
b = box(l,b,r,t)

print(b)

footprint_gdf = gpd.GeoDataFrame(gpd.GeoSeries(b), columns=['geometry'])
print(raster.crs.data)