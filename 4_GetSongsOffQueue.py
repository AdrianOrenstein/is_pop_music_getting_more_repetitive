#!/usr/bin/python3

# Reads queue.txt and writes lyrics to file 

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
import asyncio
import concurrent.futures

list_of_things = []

with open("./Data/queue.txt") as f:
    list_of_things = f.readlines()


def accessUrl(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    return soup


def parseLyricsLink(queue_object):
    lyricWebPageLink = queue_object.get('link')
    musicYear = queue_object.get('year')

    verseSoup = accessUrl(lyricWebPageLink)

    # get metadata
    pattern = re.compile(r'var utag_data={"siteSection":');

    script = verseSoup.findAll('script', text=pattern)

    regex = r"utag_data=(.+)\|\|{}"

    test_str = script[0].text

    matches = re.finditer(regex, test_str)

    musicArtistName = None
    musicAlbumTitle = None
    musicSongTitle = None

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            if groupNum == 1:
                json_data = match.group(groupNum)

                data = json.loads(json_data)

                musicArtistName = data.get(
                    'musicArtistName', 'default-artist-name')
                musicAlbumTitle = data.get(
                    'musicAlbumTitle', 'single')
                musicSongTitle = data.get(
                    'musicSongTitle', 'untitled')

    musicLyrics = ""

    Recording = False
    for p in verseSoup.findAll('p'):
        if p.get('class', 'verse'):
            if "Song Discussions" in p.text:
                Recording = False
                continue

            if "Published by" in p.text:
                Recording = True
                continue

            if Recording == True:
                musicLyrics += p.text + "\n"
                continue

    if musicArtistName == "":
        print("skip due to artist name" + lyricWebPageLink)
        return

    if musicLyrics == "":
        print("skip due to no lyrics" + lyricWebPageLink)
        return

    # Build filePath
    dataStructure = (
        musicYear + "/" + musicArtistName + "/" + musicAlbumTitle + "/" + musicSongTitle)
    dirPath = os.path.join(
        "./Data/Dataset/", re.sub('[^-a-zA-Z0-9_/]+', '', dataStructure))
    # print(dirPath)

    # Build directories
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # Build fileName
    fileName = re.sub('[^-a-zA-Z0-9_/]+',
                      '', musicSongTitle) + '.txt'

    print(re.sub('[^-a-zA-Z0-9_/]+',
                 '', dataStructure) + fileName)

    # Create file
    temp_file = open(os.path.join(dirPath, fileName), 'w')

    # Write lyrics
    temp_file.write(musicLyrics)

    temp_file.close()


def concurrency_func(queue_string):
    queue_object = json.loads(queue_string)

    parseLyricsLink(queue_object)
    return


concurrency_factor = 50


async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_factor) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                concurrency_func,
                thang
            )
            for thang in list_of_things
        ]
        for response in await asyncio.gather(*futures):
            pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
