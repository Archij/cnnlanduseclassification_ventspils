"""
@author: Arthur Stepchenko
"""

import os, gdal, sys
import itertools
import multiprocessing

in_path = '/home/arturs/Data/RGB/'
input_filename = '4114-14_1.tif'
os.mkdir('/home/arturs/Data/RGB_Tiles/')

ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

tile_size_x = 224
tile_size_y = 224

#Indices i and j
i = range(0, xsize, tile_size_x)
j = range(0, ysize, tile_size_y)

#The list contain all possible combinations of parameters.
paramlist = list(itertools.product(i,j))

#A function which will process a tuple of parameters
def translate(params):
  i = params[0]
  j = params[1]
  com_string = "gdal_translate -a_srs EPSG:3059 -a_nodata 0.0 -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
  os.system(com_string)
  return None

filelist = [file for file in os.listdir('/home/arturs/Data/RGB/') if file.endswith('.tif')]
for file in filelist:
    input_filename = file
    out_path = '/home/arturs/Data/RGB_Tiles/' + os.path.splitext(file)[0] + '/' #'/home/arturs/Data/CIR_Tiles/'
    os.mkdir(out_path)
    output_filename = os.path.splitext(file)[0]
    #Generate processes equal to the number of cores
    pool = multiprocessing.Pool()

    #Distribute the parameter sets evenly across the cores
    res  = pool.map(translate,paramlist)
