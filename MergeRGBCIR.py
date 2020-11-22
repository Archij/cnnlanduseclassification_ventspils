"""
@author: Arthur Stepchenko
"""

import os, gdal, sys
import cv2

 
subfolders = [ f.name for f in os.scandir('/home/arturs/Data/LandUse1/') if f.is_dir() ]
for subfolder in subfolders:
    filelist = [file for file in os.listdir('/home/arturs/Data/LandUse1/' + subfolder) if file.endswith('.tif')]
    for file in filelist:
         CIR_subfolder = file.partition('_tile')[0]
         filelist2 = [file2 for file2 in os.listdir('/home/arturs/Data/CIR_Tiles/' + CIR_subfolder) if file.endswith('.tif')]
         for file2 in filelist2:
               if file == file2:
                  RGB_Image = '/home/arturs/Data/LandUse1/' + subfolder + '/' + file
                  CIR_Image = '/home/arturs/Data/CIR_Tiles/' + CIR_subfolder + '/' + file2
                  outvrt = '/vsimem/stacked.vrt' #/vsimem is special in-memory virtual "directory"
                  outtif = RGB_Image
                  src = cv2.imread(RGB_Image, cv2.IMREAD_UNCHANGED)
                  red_channel = src[:,:,2]
                  green_channel = src[:,:,1]
                  blue_channel = src[:,:,0]
                  cv2.imwrite('r.tif',red_channel) 
                  cv2.imwrite('g.tif',green_channel) 
                  cv2.imwrite('b.tif',blue_channel) 
                  src = cv2.imread(CIR_Image, cv2.IMREAD_UNCHANGED)
                  cir_channel = src[:,:,0]
                  cv2.imwrite('cir.tif',cir_channel) 
                  tifs = ['r.tif', 'g.tif', 'b.tif', 'cir.tif'] 
                  outds = gdal.BuildVRT(outvrt, tifs, separate=True)
                  outds = gdal.Translate(outtif, outds)
os.remove("r.tif")
os.remove("g.tif")
os.remove("b.tif")
os.remove("cir.tif")
                