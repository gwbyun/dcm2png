#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 02:13:15 2022

@author: gw
"""

import numpy as np
import pydicom
import os
import cv2
from glob import glob
from PIL import Image


    
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)



def load_dicom(path,save_path):
    slices = [pydicom.read_file(s) for s in glob(os.path.join(path,'*.dcm'))]
    #slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]

    '''sort file'''
    slices.sort(key = lambda x: int(x.InstanceNumber))
    #Instance numbur sort
    
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])

    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices: 
        s.SliceThickness = slice_thickness
        
    
   
    '''convert '''
    for n, image in enumerate(slices):
        image = image.pixel_array.astype(float) #dicom to pixel array (slice = tuple)
        #print(image)
        #image = image.astype(np.int16)
        #image[image == -2000] = 0
        #intercept = slices[0].RescaleIntercept
        #slope = slices[0].RescaleSlope
        #if slope != 1:
        #    image = slope * image.astype(np.float64)
        #    mage = image.astype(np.int16)
        #image += np.int16(intercept)
        
        '''rescale image file'''
        rescaled_image = (np.maximum(image,0)/image.max())*255
        image = np.uint8(rescaled_image)
        image = Image.fromarray(image)
        
        create_dir(save_path)
        #cv2.imwrite(os.path.join(save_path,save_path+'{}.png'.format(n)),image)
        image.save(save_path+'/'+save_path+'{}.png'.format(n))
        #cv2.imwrite(os.path.join(save_path,'.jpg'))
        if n % 50 == 0:
            print('{} image converted'.format(n))


load_dicom('김영순 post diastolic','김영순 post diastolic_png')  #(load_path,_save_path)