#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:30:38 2018

@author: karan
"""

import gensim
import re
import os
import pandas as pd

path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Cleaned-ext-archive/'

#generating file paths  
all_topics = []
all_prob = []
all_channel=[]
all_twitterID=[]
#get_channel=str()
#twiter_id=str()      
for root, dirs, files in os.walk(path):
    for f in files:
        if os.path.splitext(f)[1].lower() == ".txt":
            file_path=os.path.join(root, f)

            #actual LDA procedure
            text_file = open(file_path, "r")
            lines = text_file.read().lower().split("\n")
            texts=[]
            for line in lines:
                texts.append(line.split())
                
            dictionary = gensim.corpora.Dictionary(texts)
            corpus = [dictionary.doc2bow(text) for text in texts]
            model = gensim.models.TfidfModel(corpus)
            corpus_tfidf = model[corpus]
            
            index = gensim.similarities.MatrixSimilarity(model[corpus])
            sims = index[corpus_tfidf]
            
            lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=9) # initialize an LSI transformation
            corpus_lsi = lsi[corpus_tfidf]
            
            twiter_id=root.split("/")[-1]
            get_channel = root.split("/")[-2]
            get_channel = get_channel.split("-")[0]
            
            topics = lsi.print_topics(9)
            lsi.save("model/"+get_channel+"_"+twiter_id)
            for topic in topics:
                split_topic=" ".join(topic[1].split("*"))
                split_topic=split_topic.split("+")
                
                for t in split_topic:
                    prob,tp = t.split()
                    all_prob.append(prob)    
                    all_topics = all_topics + re.findall('"([^"]*)"', tp)
                    all_channel.append(get_channel)
                    all_twitterID.append(twiter_id)
            print(get_channel,twiter_id)
          
channels=['fb','tw','ig','yt']
alls=[all_twitterID,all_channel,all_topics,all_prob]
a=pd.DataFrame(alls).T
col=['tw_handle',"channel","topics","prob"]
a.columns = col
for c in channels:
    col2=['tw_handle',c+"_channel",c+"_topics",c+"_prob"]
    subset=a[a['channel']==c]
    subset.columns=col2
    subset.to_csv(c+"_TM_LSI.csv",index=False,sep=";")

"""
file_path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Cleaned-ext-archive/fb-cleaned-ext/beautylish/part-00000-0d0684df-fdca-46c3-80bc-9ac41867a8bc-c000.txt'
#actual LDA procedure
text_file = open(file_path, "r")
lines = text_file.read().lower().split("\n")
texts=[]
for line in lines:
    texts.append(line.split())
    
dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
model = gensim.models.TfidfModel(corpus)
corpus_tfidf = model[corpus]

index = gensim.similarities.MatrixSimilarity(model[corpus])
sims = index[corpus_tfidf]

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=9) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]

topics = lsi.print_topics(9)

all_topics = []
    
for topic in topics:
    t=" ".join(topic[1].split("*"))
    t=" ".join(t.split("+"))
    all_topics = all_topics + re.findall('"([^"]*)"', t)

"""
