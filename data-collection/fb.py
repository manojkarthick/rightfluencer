#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:45:46 2018

@author: kartiw
"""

import facebook
import pandas as pd
import os

outdir = "/home/kartiw/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/Karan/facebook-scrapping/data"
if not os.path.exists(outdir):
    os.mkdir(outdir)


token = "EAAcSYjNVPtcBAKqBYh7xGoXy0KcAHaSKbi5QmhBnf6ctMacdQUHdxn2jCYSdzqu5XQzOi3ZAjd57SwdkQZCrtG2e1cesYtQb2PmaMejCc3dZCc2P72BmPWFWAZBDKZA8zb7ZCNy19GWTibtiZAdCanSqmrqEqwR80YnZBBniwdeWgwZDZD"


#gets user posts with captions and image links, plus other meta infromation and user profile info
#data is in jason format, i didnt transform it yet, because we might just put this in the db as it is
#if a different structure is reqired let me know.
 
def get_fbPosts(user):
    graph = facebook.GraphAPI(access_token=token, version=2.7)
    #influencer = graph.request(url)
    profile = graph.get_object(id=user, fields='id,name,about,link,location,hometown,website', limit=100)
    posts = graph.get_connections(profile['id'], connection_name='posts', fields='caption,created_time,description,from,link,message,object_id,parent_id,permalink_url,picture,privacy,place,properties,shares,source,status_type,story,to,type,with_tags,total_count,reactions,comments', limit='100') 

    return profile, posts['data']

def extract_data(profile, posts, twitter_handle, influencer, category, fb_handle):
    
    default="NA"
    col=['twitter_handle','fb_handle','fb_name','fb_category','fb_no_of_comments','fb_time_created','fb_description','fb_post_link','fb_img_link','fb_shares','fb_type']
    
    dataset_list=[]
    #dataset_dict=dict()
    #df=pd.DataFrame(columns=col)
    for post in posts:
        
        try:
            no_of_comments = len(post['comments']['data'])
        except:
            no_of_comments = default
        
        try:
            time_created = post['created_time']
        except:
            time_created = default
        
        try:
            #Description = post['message']
            Description = " ".join(post['message'].split(','))
        except:
            Description=default
        
        try:
            post_link = post['permalink_url']
        except:
            post_link=default
        
        try:
            img_link = post['picture']
        except:
            img_link = default
        
        try:
            shares = post['shares']['count']
        except:
            shares=default    
        
        try:
            post_type = post['type']
        except:
            post_type=default
    
        #write to csv
        dataset_list.append([twitter_handle,fb_handle,influencer,category,no_of_comments,time_created,Description,post_link,img_link,shares,post_type])
       
    #dataset_pd=dataset_list
    dataset_pd=pd.DataFrame(dataset_list,columns=col)
    outname=influencer+".csv"
    name = os.path.join(outdir, outname)
    dataset_pd.to_csv(name,index=False,sep=";")
    return influencer




# Main()
influencerList=pd.read_csv("/home/kartiw/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/data/influencer_list.csv")

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
        
        profile, posts = get_fbPosts(fb_handle)
        done=extract_data(profile, posts, twitter_handle, influencer, category, fb_handle)
        print(done)

#user="La-Dolce-Vita-Blog-297190888239"
#profile, posts = get_fbPosts(user)

