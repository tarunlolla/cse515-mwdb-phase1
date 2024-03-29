#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:13:53 2019

@author: tarunlolla
"""
import pymongo
import scipy
import cv2
import numpy as np
import sys
import os
np.set_printoptions(threshold=sys.maxsize);
import cm
import sift
import time

def main():
    work_dir=input("Enter the location of dataset:")
    conn=pymongo.MongoClient('localhost',27017)
    db=conn.phase1
    collection1=db.color_moments
    collection2=db.sift
    collection3=db.img_path
    color_moments={}
    sift_des={}
    for i in os.listdir(work_dir):
        collection3.insert_one({str(i.replace('.','')):work_dir+'/'+i})
        print("Computing color moments for "+i)
        x=cm.compute_cm(work_dir+'/'+i,100,100)
        color_moments[str(i.replace('.',''))]=x
        collection1.insert_one({ '_id' : str(i.replace('.','')), 'y_cm' : x[0], 'u_cm' : x[1], 'v_cm':x[2] })
        print("Finding descriptor vectors for "+i)
        y=sift.compute_des(work_dir+'/'+i)
        sift_des[str(i.replace('.',''))]=list(y)
        collection2.insert_one({ '_id' : str(i.replace('.','')), 'descr' : list(y) })

if __name__ == '__main__':
    main()



"""
/home/tarunlolla/MWDB/Project/Hands_Test
/home/tarunlolla/MWDB/Project/small_dataset
Comments :: This code demonstrates how the blocks are being created.

import cv2
img=cv2.imread('/home/tarunlolla/MWDB/Project/Hand_0005140.jpg');
img[0:100,0:100]=[0,0,255];
img[0:100,100:200]=[0,0,0];
img[100:200,100:200]=[0,255,0];
img[200:300,200:300]=[255,0,0];
cv2.imshow('image',img);cv2.waitKey(0);cv2.destroyAllWindows();
"""
