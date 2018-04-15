#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 11:15:36 2018

@author: karan
"""

import facebook
import pandas as pd
import datetime
import requests
import random

token = "EAAcSYjNVPtcBAKqBYh7xGoXy0KcAHaSKbi5QmhBnf6ctMacdQUHdxn2jCYSdzqu5XQzOi3ZAjd57SwdkQZCrtG2e1cesYtQb2PmaMejCc3dZCc2P72BmPWFWAZBDKZA8zb7ZCNy19GWTibtiZAdCanSqmrqEqwR80YnZBBniwdeWgwZDZD"


#a=requests.get("https://graph.facebook.com/v2.12/MKBHD?fields=name,fan_count&access_token="+token)

influencerList=pd.read_csv("/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Backup/project-data/project-data/main-csv-data/influencer_list.csv")

profiles_list=[]
influencer_l =[]

now=datetime.datetime.now()
month = now.strftime("%b")
date = now.strftime("%d")
today = month+"-"+date

profiles_list.append([today])
influencer_l.append("Date")

for index, row in influencerList.iterrows():
    
    influencer = row['Influencer']
    category = row['Category']
    fb_url = row['Facebook']
    twitter_url = row['Twitter']
    
    splits = fb_url.split('/')
    splits2=twitter_url.split('/')
    
    if fb_url:
        if fb_url.endswith('/'):
            fb_handle = splits[-2]
        else:
            fb_handle = splits[-1]
    else:
        fb_handle = None
    
    if twitter_url:
        if twitter_url.endswith('/'):
            twitter_handle = splits2[-2]
        else:
            twitter_handle = splits2[-1]
    else:
        twitter_handle = None
        
    like_info=requests.get("https://graph.facebook.com/v2.12/"+str(fb_handle)+"?fields=name,fan_count&access_token="+token)
    like_info = like_info.json()
    try:
        profiles_list.append([like_info['fan_count']])   
        influencer_l.append(twitter_handle)
    except:
        profiles_list.append([""])
        influencer_l.append(twitter_handle)

l=pd.DataFrame(profiles_list).T
l.columns=influencer_l


growth = pd.read_csv("audience_growth.csv")
growth = pd.concat([growth,l],axis=0)
growth.to_csv("audience_growth.csv",index=False)