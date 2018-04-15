#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:08:44 2018

@author: karan
"""

import facebook
import pandas as pd
import os
import requests
import json

token = "EAAcSYjNVPtcBAKqBYh7xGoXy0KcAHaSKbi5QmhBnf6ctMacdQUHdxn2jCYSdzqu5XQzOi3ZAjd57SwdkQZCrtG2e1cesYtQb2PmaMejCc3dZCc2P72BmPWFWAZBDKZA8zb7ZCNy19GWTibtiZAdCanSqmrqEqwR80YnZBBniwdeWgwZDZD"
#token='EAACEdEose0cBADLZCyZANNDOto1nlqFCG8kvaLjZCqZBgOVJBzROWHAISa0lLooPCR7ZCcWxpbZBPK5uiFbnTDZBRw14rUT1HxqqZAbx02ZBk1sRIfPQaP344gEDOyNgBEMMqRlkDVxCW7uHSsylufYZA4kCNrj6O0gKu9UTI0JtexEIiFg2ISKHP7OE56WFALZAJkZD'
def get_id(user):
    graph = facebook.GraphAPI(access_token=token, version=2.7)
    #influencer = graph.request(url)
    userid = graph.get_object(id=user, fields='id', limit=100)
    return userid
#a=requests.get("https://graph.facebook.com/v2.12/MKBHD?fields=name,fan_count&access_token="+token)

influencerList=os.listdir("/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Backup/project-data/project-data/facebook-data")

tw_handle=[]
fb_handle=[]


for file in influencerList:
    if file != "MKBHD":
        continue
    file_path=os.path.join('/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Backup/project-data/project-data/facebook-data',file)
    dataf = open(file_path, 'r')
    data=dataf.read().splitlines()
    dataf.close()
    for d in data:
        data2=json.loads(d)
       
        try:
            uid=get_id(data2['fb_handle'])
            postid=data2['fb_post_link'].split('/')[-1]
            total=0
            #print("https://graph.facebook.com/v2.12/"+str(uid['id'])+"_"+postid+"/comments?summary=1&access_token="+token)
            No_comment=requests.get("https://graph.facebook.com/v2.12/"+str(uid['id'])+"_"+postid+"/comments?summary=1&access_token="+token)
            No_comment = No_comment.json()
            #print(No_comment)
            try:
                total = No_comment['summary']['total_count']
            except:
                total = data2['fb_no_of_comments']
            
            data2['fb_no_of_comments']=total
            
            with open(os.path.join("data",str(file)), 'a') as f:
                f.write(json.dumps(data2))
                f.write("\n")
            #f.close()
        except:
            with open(os.path.join("data",str(file)), 'a') as f:
                f.write(json.dumps(data2))
                f.write("\n")
            #f.close()
        
    
    break
    print(file)

    