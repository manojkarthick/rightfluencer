# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gensim
import os
import re
import pandas as pd
import pyLDAvis.gensim

#recursively itterates thur the folders and gets topics for every data-source separately

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
            lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=9, update_every=1, chunksize=10000, passes=10)
            #print(lda.print_topics(num_topics=10, num_words=10))
            twiter_id=root.split("/")[-1]
            get_channel = root.split("/")[-2]
            get_channel = get_channel.split("-")[0]
            
            topics = lda.print_topics(9)
            lda.save("model/"+get_channel+"_"+twiter_id)

            lda_plot=pyLDAvis.gensim.prepare(lda, corpus, dictionary)
            pyLDAvis.save_html(lda_plot,fileobj="html_plots/"+get_channel+"_"+twiter_id+".html",template_type='general', visid=get_channel+"_"+twiter_id)
            
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


channels=['fb','tw','ig']
alls=[all_twitterID,all_channel,all_topics,all_prob]
a=pd.DataFrame(alls).T
col=['tw_handle',"channel","topics","prob"]
a.columns = col
for c in channels:
    col2=['tw_handle',c+"_channel",c+"_topics",c+"_prob"]
    subset=a[a['channel']==c]
    subset.columns=col2
    subset.to_csv(c+"_TM_LDA.csv",index=False,sep=";")
   
#col=['tw_handle',get_channel.join("_channel"),get_channel.join("_topics"),get_channel.join("_prob")]
#alls=[all_twitterID,all_channel,all_topics,all_prob]
#a=pd.DataFrame(alls, columns=col).T
#a.to_csv(get_channel.join("_TM.csv"),index="False",sep=";")    
        
"""

#for testing on a single file
file_path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/Cleaned-ext-archive/fb-cleaned-ext/MKBHD/part-00000-471531eb-bd56-437c-b76e-aa482b8b01df-c000.txt'
#actual LDA procedure
text_file = open(file_path, "r")
lines = text_file.read().lower().split("\n")
texts=[]
for line in lines:
    texts.append(line.split())
    
dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, update_every=1, chunksize=10000, passes=10)
#print(lda.print_topics(num_topics=10, num_words=10))
topics = lda.print_topics(10)

all_topics = []
all_prob = []
    
for topic in topics:
    split_topic=" ".join(topic[1].split("*"))
    split_topic=split_topic.split("+")
    
    for t in split_topic:
        prob,tp = t.split()
        all_prob.append(prob)    
        all_topics = all_topics + re.findall('"([^"]*)"', tp)

#lda.get_term_topics("travel")
        
for i in zip(all_topics,all_prob):
    print(i)
"""
