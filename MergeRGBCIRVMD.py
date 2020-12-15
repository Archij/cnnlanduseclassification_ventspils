"""
@author: Arthur Stepchenko
"""

import os, gdal, sys, shutil
from vmd2d import VMD_2D
import numpy as np
import cv2

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
         CIR_subfolder = file.partition('_tile')[0]
         filelist2 = [file2 for file2 in os.listdir('/home/arturs/Data/CIR_Tiles/' + CIR_subfolder) if file.endswith('.tif')]
         for file2 in filelist2:
               if file == file2:
                    RGB_Image = '/home/arturs/Data/LandUse1/' + subfolder + '/' + file
                    CIR_Image = '/home/arturs/Data/CIR_Tiles/' + CIR_subfolder + '/' + file2
                    print(str(num) + ": " + RGB_Image)
                    shutil.copy(CIR_Image,  '/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_CIR.tif') 
                    src = cv2.imread(RGB_Image, cv2.IMREAD_UNCHANGED)
                    red_channel = src[:,:,2]
                    green_channel = src[:,:,1]
                    blue_channel = src[:,:,0]
                    src = cv2.imread(CIR_Image, cv2.IMREAD_UNCHANGED)
                    cir_channel = src[:,:,0]
                    #. Run VMD 
                    u, u_hat, omega = VMD_2D(np.array(red_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u11.tif', np.array((u[0,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u12.tif', np.array((u[1,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u13.tif', np.array((u[2,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u14.tif', np.array((u[3,:,:]), dtype='float32'))
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u15.tif', np.array((u[4,:,:]), dtype='float32')) 
                    u, u_hat, omega = VMD_2D(np.array(green_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u21.tif', np.array((u[0,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u22.tif', np.array((u[1,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u23.tif', np.array((u[2,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u24.tif', np.array((u[3,:,:]), dtype='float32'))
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u25.tif', np.array((u[4,:,:]), dtype='float32')) 
                    u, u_hat, omega = VMD_2D(np.array(blue_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u31.tif', np.array((u[0,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u32.tif', np.array((u[1,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u33.tif', np.array((u[2,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u34.tif', np.array((u[3,:,:]), dtype='float32'))
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u35.tif', np.array((u[4,:,:]), dtype='float32')) 
                    u, u_hat, omega = VMD_2D(np.array(cir_channel,  dtype='float32'), alpha, tau, K, DC, init, tol)
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u41.tif', np.array((u[0,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u42.tif', np.array((u[1,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u43.tif', np.array((u[2,:,:]), dtype='float32')) 
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u44.tif', np.array((u[3,:,:]), dtype='float32'))
                    cv2.imwrite('/home/arturs/Data/LandUse1/' + subfolder + '/' + os.path.splitext(file)[0] + '_u45.tif', np.array((u[4,:,:]), dtype='float32'))
                    num = num+1
