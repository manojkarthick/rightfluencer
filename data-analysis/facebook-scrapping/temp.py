#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 12:37:33 2018

@author: karan
"""

import pandas as pd
import json

path = "/home/karan/Karan/anaconda-workspace/python3-wokspace/CMPT733/influencers-project/Karan/facebook-scrapping/data/pewdiepie"

dataf = open(path, 'r')
data=dataf.read().splitlines()
dataf.close()
js=[]

for d in data:
    js.append(json.loads(d))


df=pd.DataFrame(js)