#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:12:53 2018

@author: karan
"""

import pandas as pd
import os
import json

numwords=25

path = "/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/LSI-op"   
tw_path = os.path.join(path,"tw_TM_LSI.csv")
fb_path =  os.path.join(path,"fb_TM_LSI.csv")
yt_path = os.path.join(path,"yt_TM_LSI.csv")
ig_path = os.path.join(path,"ig_TM_LSI.csv")

col= ["tw_handle",'channel','topic','prob']
tw = pd.read_csv(tw_path, sep=";")
fb = pd.read_csv(fb_path, sep=";")
yt = pd.read_csv(yt_path, sep=";")
ig = pd.read_csv(ig_path, sep=";")

tw.columns = fb.columns = yt.columns = ig.columns = col

influencers = list(tw['tw_handle'].unique())

df=pd.concat([tw,fb,yt,ig], ignore_index=True)

for influencer in influencers:
    outdict=dict()
    newdf = df[df['tw_handle']==influencer]
    newdf = newdf.drop_duplicates(subset='topic').sort_values(by='prob', ascending=[0])
    newdf = newdf.dropna()
    topics = list(newdf['topic'].head(numwords))
         
    for t in topics:
        try:
            int(t)
            topics.remove(t)
        except:
            pass
    
    outdict['tw_handle']=influencer
    outdict['topics']=topics
    
    with open("topic_pills", 'a') as f:
        f.write(json.dumps(outdict))
        f.write("\n")
    f.close()
    
