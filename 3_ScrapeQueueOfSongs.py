#!/usr/bin/python3

# Searches through Artist_[A-Z] and queues downloads
# for next script

import requests
import fileinput
import os
import string
import re
import json
import unicodedata
from bs4 import BeautifulSoup
from unidecode import unidecode
import pdb


def accessUrl(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    # print (soup.title.string + '\n---');
    return soup


def findNextPage(soup):
    # now find next page
    for nextPage in soup.findAll('p'):
        for field in nextPage.findAll('a', {"class": "button next"}):
            url_input = field['href']
    return url_input


searchSeq = 'abcdefghijklmnopqrstuvwxyz'

for char in searchSeq:
    # Read from Artist Info
    fileinput = './Data/Artist_' + char

    # Read artist list
    with open(fileinput) as f:
        content = f.readlines()

    # Search artists
    for line in content:
        print("\nLine: " + line.strip() + "\n");
        # Open artist
        req = requests.get(line)
        soup = BeautifulSoup(req.text, "lxml")

        while True:
            # Continue writing artists untill fail
            try:
                # Find song links
                table = soup.find("table").find("tbody")

                # In each row
                for row in table.findAll("tr"):
                    # path
                    musicYear = 0000

                    # find musicYear\
                    col2 = row.findAll('td')
                    for x in col2:
                        if len(x.text.strip()) == 4:
                            # print musicYear
                            musicYear = x.text.strip()

                    # get link
                    lyricWebPageLink = None

                    for col1 in row.findAll('a'):
                        lyricWebPageLink = col1['href']

                    queueObj = {"link": lyricWebPageLink, "year": musicYear}

                    with open("./Data/queue.txt", "a") as myqueue:
                        myqueue.write(json.dumps(queueObj) + "\n")

                # Continue to next page
                soup = accessUrl(findNextPage(soup))

            except:
                break
