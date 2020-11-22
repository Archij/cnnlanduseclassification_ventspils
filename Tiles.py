"""
@author: Arthur Stepchenko
"""

import os, gdal, sys
 
in_path = '/home/arturs/Data/RGB/'
input_filename = sys.argv[1]
 
out_path = sys.argv[2]
os.mkdir(out_path)
output_filename = sys.argv[3] + '_tile_'
 
tile_size_x = 224
tile_size_y = 224
 
ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize
 
for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -a_srs EPSG:3059 -a_nodata 0.0 -of JPEG -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)