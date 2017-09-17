#!/usr/bin/python3

# Gets the lists of artists A-Z and writes to searchSeq

import requests
import os
import string
from bs4 import BeautifulSoup
 
searchSeq = 'abcdefghijklmnopqrstuvwxyz'

f = open('./Data/searchSeq', 'w')

for char in searchSeq:
    # Find all music lists
    link = 'http://www.metrolyrics.com/artists-' + char + '-1' + '.html'
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    print(link)
    f.write(link + '\n');
    
f.close();