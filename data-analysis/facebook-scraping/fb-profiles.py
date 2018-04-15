#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 09:54:12 2018

@author: kartiw
"""

import facebook
import pandas as pd
import os

outdir = "/home/kartiw/Karan/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/Karan/facebook-scrapping/data"
if not os.path.exists(outdir):
    os.mkdir(outdir)


token = "EAAcSYjNVPtcBAKqBYh7xGoXy0KcAHaSKbi5QmhBnf6ctMacdQUHdxn2jCYSdzqu5XQzOi3ZAjd57SwdkQZCrtG2e1cesYtQb2PmaMejCc3dZCc2P72BmPWFWAZBDKZA8zb7ZCNy19GWTibtiZAdCanSqmrqEqwR80YnZBBniwdeWgwZDZD"


#gets user posts with captions and image links, plus other meta infromation and user profile info
#data is in jason format, i didnt transform it yet, because we might just put this in the db as it is
#if a different structure is reqired let me know.
 
def get_fbPosts(user):
    graph = facebook.GraphAPI(access_token=token, version=2.7)
    profile = graph.get_object(id=user, fields='id,name,about,link,location,hometown,website, fan_count', limit=100)
    return profile


def extract_data(profile, twitter_handle,fb_handle, influencer, category):
    
    default="NA"
    
    try:
        #about = profile['about']
        about = " ".join(profile['about'].split(','))
    except:
        about = default
    
    try:
        city = profile['location']['city']
    except:
        city = default
        
    try:
        state = profile['location']['state']
    except:
        state = default
        
    try:
        country = profile['location']['country']
    except:
        country = default
    
    try:
        longitude = profile['location']['longitude']
    except:
        longitude = default
        
    try:
        latitude = profile['location']['latitude']
    except:
        latitude = default
        
    try:
        #hometown = profile['hometown']
        hometown = " ".join(profile['hometown'].split(','))
    except:
        hometown=default
    
    try:
        website = profile['website']
    except:
        website=default
    

    return [twitter_handle,fb_handle,influencer,category,about,city,state,country,longitude,latitude,hometown,website]


influencerList=pd.read_csv("/home/kartiw/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/data/influencer_list.csv")

profiles_list=[]

for index, row in influencerList.iterrows():
    influencer = row['Influencer']
    category = row['Category']
    fb_url = row['Facebook']
    twitter_url = row['Twitter']
    
    if fb_url == "null":
        pass
    else:
    
        splits = fb_url.split('/')
        splits2=twitter_url.split('/')
        
        if fb_url:
            if fb_url.endswith('/'):
                fb_handle = splits[-2]
            else:
                fb_handle = splits[-1]
        else:
            fb_handle = None
            
        #to get the twitter handles
        if twitter_url:
            if twitter_url.endswith('/'):
                twitter_handle = splits2[-2]
            else:
                twitter_handle = splits2[-1]
        else:
            twitter_handle = None
        
        profile = get_fbPosts(fb_handle)
        profiles_list.append(extract_data(profile,twitter_handle,fb_handle,influencer,category))
        

col=['twitter_handle','fb_handle','fb_name','fb_category','fb_about','fb_city','fb_state','fb_country','fb_longitude','fb_latitude','fb_hometown','fb_website']
profiles = pd.DataFrame(profiles_list,columns=col)

outdir = "/home/kartiw/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/Karan/facebook-scrapping/data"
outname="fb-profiles.csv"
name = os.path.join(outdir, outname)
profiles.to_csv(name,index=False,sep=";")