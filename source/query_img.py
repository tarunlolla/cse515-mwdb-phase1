#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 15:44:58 2019

@author: tarunlolla
"""

import pymongo
import numpy as np
conn=pymongo.MongoClient('localhost',27017)
db=conn.phase1
collection_cm=db.color_moments
collection_sift=db.sift

def eucl_dist_cm(img1,img2):
    img1_id=img1[0]
    img1_vector=img1[1]
    img2_id=img2[0]
    img2_vector=img2[1]
    dist=0.0
    for i in range(0,3):
        dist += (img1_vector[i]-img2_vector[i])**2
    return img2_id,dist**(1/2)

def query_img_cm(qimg_id,k):
    query={ '_id' : qimg_id }
    doc=collection_cm.find(query)
    for x in doc:
        query_y=x['y_cm']
        query_u=x['u_cm']
        query_v=x['v_cm']
        query_img_vector=[qimg_id,query_y+query_u+query_v]
    condition='$ne'
    all_images_query=collection_cm.find({'_id' : {condition: qimg_id}})
    all_images=[]
    for i in all_images_query:
        all_images.append([i['_id'],i['y_cm']+i['u_cm']+i['v_cm']])
    dist=[]
    for i in all_images:
        x,y=eucl_dist_cm(query_img_vector,i)
        dist.append([x,y])
    dist=sorted(dist,key=lambda i:i[1])
    return dist[:k]

def eucl_dist_sift(img1,img2):
    img1_id=img1[0]
    img1_vector=img1[1]
    img2_id=img2[0]
    img2_vector=img2[1]
    dist=0.0
    for i in range(0,len(img1_vector)):
        dist += (img1_vector[i]-img2_vector[i])**2
    return img2_id,dist**(1/2)


def query_img_sift(qimg_id,k):
    query={ '_id' : qimg_id }
    doc=collection_sift.find(query)
    for x in doc:
        query_img=[qimg_id,list(np.mean(x['descr'],axis=0))]
    condition='$ne'
    all_images_query=collection_sift.find({'_id' : {condition: qimg_id}})
    all_images=[]
    for i in all_images_query:
        all_images.append([i['_id'],list(np.mean(i['descr'],axis=0))])
    dist=[]
    for i in all_images:
        a,b=eucl_dist_sift(query_img,i)
        dist.append([a,b])
    dist=sorted(dist,key=lambda i:i[1])
    return dist[:k]