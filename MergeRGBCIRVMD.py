"""
@author: Arthur Stepchenko
"""

import os, gdal, sys
import cv2
from vmd2d import VMD_2D
import numpy as np

#. some sample parameters for VMD  
alpha = 5000       # moderate bandwidth constraint  
tau = 0.01            # noise-tolerance (no strict fidelity enforcement)  
K = 5            # 5 modes  
DC = 1             # DC part imposed  f
init = 0           # initialize omegas uniformly  
tol = 0.000001
num = 1
 
subfolders = [ f.name for f in os.scandir('/home/arturs/Data/LandUse1/') if f.is_dir() ]
for subfolder in subfolders:
    filelist = [file for file in os.listdir('/home/arturs/Data/LandUse1/' + subfolder) if file.endswith('.tif')]
    for file in filelist:
        RGB_Image = '/home/arturs/Data/LandUse1/' + subfolder + '/' + file
        print(str(num) + ": " + RGB_Image)
        outvrt = '/vsimem/stacked.vrt' #/vsimem is special in-memory virtual "directory"
        outtif = RGB_Image
        src = cv2.imread(RGB_Image, cv2.IMREAD_UNCHANGED)
        red_channel = src[:,:,0]
        green_channel = src[:,:,1]
        blue_channel = src[:,:,2]
        cir_channel = src[:,:,3]
        cv2.imwrite('r.tif',np.array(red_channel, dtype='float32')) 
        cv2.imwrite('g.tif',np.array(green_channel, dtype='float32')) 
        cv2.imwrite('b.tif',np.array(blue_channel, dtype='float32'))
        cv2.imwrite('cir.tif',np.array(blue_channel, dtype='float32'))
        #. Run VMD 
        u, u_hat, omega = VMD_2D(np.array(red_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
        cv2.imwrite('u11.tif', np.array((u[0,:,:]), dtype='float32')) 
        cv2.imwrite('u12.tif', np.array((u[1,:,:]), dtype='float32')) 
        cv2.imwrite('u13.tif', np.array((u[2,:,:]), dtype='float32')) 
        cv2.imwrite('u14.tif', np.array((u[3,:,:]), dtype='float32'))
        cv2.imwrite('u15.tif', np.array((u[4,:,:]), dtype='float32')) 
        u, u_hat, omega = VMD_2D(np.array(green_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
        cv2.imwrite('u21.tif', np.array((u[0,:,:]), dtype='float32')) 
        cv2.imwrite('u22.tif', np.array((u[1,:,:]), dtype='float32')) 
        cv2.imwrite('u23.tif', np.array((u[2,:,:]), dtype='float32')) 
        cv2.imwrite('u24.tif', np.array((u[3,:,:]), dtype='float32'))
        cv2.imwrite('u25.tif', np.array((u[4,:,:]), dtype='float32')) 
        u, u_hat, omega = VMD_2D(np.array(blue_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
        cv2.imwrite('u31.tif', np.array((u[0,:,:]), dtype='float32')) 
        cv2.imwrite('u32.tif', np.array((u[1,:,:]), dtype='float32')) 
        cv2.imwrite('u33.tif', np.array((u[2,:,:]), dtype='float32')) 
        cv2.imwrite('u34.tif', np.array((u[3,:,:]), dtype='float32'))
        cv2.imwrite('u35.tif', np.array((u[4,:,:]), dtype='float32')) 
        u, u_hat, omega = VMD_2D(np.array(cir_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
        cv2.imwrite('u41.tif', np.array((u[0,:,:]), dtype='float32')) 
        cv2.imwrite('u42.tif', np.array((u[1,:,:]), dtype='float32')) 
        cv2.imwrite('u43.tif', np.array((u[2,:,:]), dtype='float32')) 
        cv2.imwrite('u44.tif', np.array((u[3,:,:]), dtype='float32'))
        cv2.imwrite('u45.tif', np.array((u[4,:,:]), dtype='float32'))
        tifs = ['r.tif', 'g.tif', 'b.tif', 'cir.tif', 'u11.tif', 'u12.tif', 'u13.tif', 'u14.tif', 'u15.tif', 'u21.tif', 'u22.tif', 'u23.tif',
        'u24.tif', 'u25.tif', 'u31.tif', 'u32.tif', 'u33.tif', 'u34.tif', 'u35.tif', 'u41.tif', 'u42.tif', 'u43.tif', 'u44.tif', 'u45.tif'] 
        outds = gdal.BuildVRT(outvrt, tifs, separate=True)
        translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine("-co COMPRESS=LZW"))
        outds = gdal.Translate('/home/arturs/Data/LandUse2/' + subfolder + '/' + file, outds, options=translateoptions)  
        num = num+1
os.remove("r.tif")
os.remove("g.tif")
os.remove("b.tif")
os.remove("cir.tif")
os.remove("u11.tif")
os.remove("u12.tif")
os.remove("u13.tif")
os.remove("u14.tif")
os.remove("u15.tif")
os.remove("u21.tif")
os.remove("u22.tif")
os.remove("u23.tif")
os.remove("u24.tif")
os.remove("u25.tif")
os.remove("u31.tif")
os.remove("u32.tif")
os.remove("u33.tif")
os.remove("u34.tif")
os.remove("u35.tif")
os.remove("u41.tif")
os.remove("u42.tif")
os.remove("u43.tif")
os.remove("u44.tif")
os.remove("u45.tif")