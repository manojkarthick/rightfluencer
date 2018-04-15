#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 17:18:14 2018

@author: karan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:10:13 2018

@author: karan
"""

import gensim
import os
import re
import pandas as pd

path = "/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Cleaned-ext-yt/yt-cleaned-ext/"
all_topics = []
all_prob = []
all_channel=[]
all_twitterID=[]
data=[]
#get_channel=str()
#twiter_id=str()
dirs = os.listdir(path)    
num=1
for d in dirs:
    texts=[]
    inner_folder = os.path.join(path,d)
    inner_dir = os.listdir(inner_folder)
    if not inner_dir:
        pass
    else:
        for in_d in inner_dir:
            if not in_d.startswith("."):
                for f in os.listdir(os.path.join(inner_folder,in_d)):
                    if f.startswith("part"):
                        
                        file_path=os.path.join(inner_folder,in_d, f)
                        text_file = open(file_path, "r")
                        lines = text_file.read().lower().split("\n")
                        
                        for line in lines:
                            texts.append(line.split())
                    #print(f)
        dictionary = gensim.corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        model = gensim.models.TfidfModel(corpus)
        corpus_tfidf = model[corpus]
        
        index = gensim.similarities.MatrixSimilarity(model[corpus])
        sims = index[corpus_tfidf]
        
        lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=9) # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]
        twiter_id=d
        get_channel = "yt"
        
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
        #print(in_d)
    print(d,num)
    num=num+1

alls=[all_twitterID,all_channel,all_topics,all_prob]
a=pd.DataFrame(alls).T
col=['tw_handle',"yt_channel","yt_topics","yt_prob"]
a.columns = col
a.to_csv("yt_TM_LSI.csv",index=False,sep=";")
 

