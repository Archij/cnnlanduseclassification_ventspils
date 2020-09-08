import os, gdal, sys
from pathlib import Path
 
 
in_path = '/home/arturs/Data/CIR/'
 
tile_size_x = 224
tile_size_y = 224

filelist = [file for file in os.listdir(in_path) if file.endswith('.tif')]
for file in filelist:
    
    out_path = '/home/arturs/Data/CIR_Tiles/' + Path(file).stem + '/'
    os.mkdir(out_path)
 
    ds = gdal.Open(in_path + file);
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize
	
    output_filename = Path(file).stem + '_tile_'
 
    for i in range(0, xsize, tile_size_x):
         for j in range(0, ysize, tile_size_y):
              com_string = "gdal_translate -a_srs EPSG:3059 -a_nodata 0.0 -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(file) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
              os.system(com_string)
