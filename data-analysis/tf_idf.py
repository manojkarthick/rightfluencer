#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:30:38 2018

@author: karan
"""

import gensim
import re


file_path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/cleaned_data/facebook-data/MKBHD/part-00000-91489971-f246-4a3f-bcfe-8bc4a22e4178-c000.txt'
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

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]

topics = lsi.print_topics(10)

all_topics = []
    
for topic in topics:
    t=" ".join(topic[1].split("*"))
    t=" ".join(t.split("+"))
    all_topics = all_topics + re.findall('"([^"]*)"', t)

