#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:15:00 2018

@author: kartiw
"""

from klout import *

def get_score(twitter_handle):
    
    key = 'qzcujyjgy7b554kw9htud9ny'
    
    # Make the Klout object
    k = Klout(key, secure=True)
    
    # Get kloutId of the user by inputting a twitter screenName
    kloutId = k.identity.klout(screenName=twitter_handle).get('id')
    
    # Optionally a timeout parameter (seconds) can also be sent with all calls
    score = k.user.score(kloutId=kloutId, timeout=5).get('score')
    
    return score
    

print(get_score("mkbhd"))