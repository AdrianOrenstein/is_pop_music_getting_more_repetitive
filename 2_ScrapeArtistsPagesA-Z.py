#!/usr/bin/python3

# For every A-Z artist, get all artists under that alphabet
# and write to Artist_[A-Z]

import requests
import fileinput
import os
import string
from bs4 import BeautifulSoup
from unidecode import unidecode

def accessUrl(url):
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "lxml")
	 
	# print (soup.title.string + '\n---');
	return soup;


def findArtistList(soup):
	# Find song links
	table = soup.find("table")
	linkStringArr = []

	for row in table.findAll("tr"):
		for link in row.findAll('a'):
			print(link['href']);
			linkStringArr.append(link['href']);

	return linkStringArr;


def findNextPage(soup):
	# now find next page
	for nextPage in soup.findAll('p'):
		for field in nextPage.findAll('a', {"class" : "button next"} ):
			url_input = field['href'];
	return url_input;


def findAndWriteArtistURLs(soup):
	while True:
			# Access list of artists
			listOfArtists = findArtistList(soup);

			# Write artist links
			for artistLink in listOfArtists:
				artistFile.write(artistLink + '\n');

			# Continue writing artists untill fail
			try:
				# To print current page
				# print(findNextPage(soup));
				soup = accessUrl(findNextPage(soup));
			except:
				print ('Done');
				break

	return


with open("./Data/searchSeq") as f:
	workDirectory = os.getcwd();

	for line in f:
		# Get artist dir
		artistsDir = './Data/Artist_'+line[-9:-8];

		# make artist File
		artistFile = open(artistsDir, 'w');

		# get URL
		soup = accessUrl(line);

		# Begin finding and writing artist URLS
		while True:
			# Access list of artists
			listOfArtists = findArtistList(soup);

			# Write artist links
			for artistLink in listOfArtists:
				artistFile.write(artistLink + '\n');

			# Continue writing artists untill fail
			try:
				# To print current page
				# print(findNextPage(soup));
				soup = accessUrl(findNextPage(soup));
			except:
				print ('Done');
				break

		# Done with artist file
		artistFile.close();

f.close()


