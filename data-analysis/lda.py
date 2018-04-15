# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gensim
import os
import re


#recursively itterates thur the folders and gets topics for every data-source separately
"""
path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/cleaned_data/'

#generating file paths        
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
            lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, update_every=1, chunksize=10000, passes=10)
            print(lda.print_topics(num_topics=10, num_words=10))
            
            topics = lda.print_topics(10)

            all_topics = []
                
            for topic in topics:
                t=" ".join(topic[1].split("*"))
                t=" ".join(t.split("+"))
                all_topics = all_topics + re.findall('"([^"]*)"', t)



"""

#for testing on a single file
file_path='/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/My project folder/cleaned_data/facebook-data/MKBHD/part-00000-91489971-f246-4a3f-bcfe-8bc4a22e4178-c000.txt'
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
    
for topic in topics:
    t=" ".join(topic[1].split("*"))
    t=" ".join(t.split("+"))
    all_topics = all_topics + re.findall('"([^"]*)"', t)

#lda.get_term_topics("travel")
