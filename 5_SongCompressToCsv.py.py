#!/usr/bin/python3

# Analyses the Dataset, recording data to lyricDataset.csv

import fileinput
import os
import string
import glob
import re
from timeit import default_timer as timer

# Recursively go through all directories
# Get the .txt file
# make compression function, write to csv
# get: year,arist,album,song,origionalSize,compressedSize,compressedRatio
# write: lyricDataset.csv

lyricDatasetCSV = open('lyricDataset.csv', 'w')

lyricDatasetCSV.write('Year,Artist,Album,Song,OrigionalSize,CompressedSize,CompressedRatio\n')

# total = 1214294
calculatedSongs = 0;
errors = 0;
start = timer()

for fileName in glob.iglob('./Data/Dataset/*/*/*/*/*.txt', recursive=False):
	try:
		# Read file
		with open(fileName, 'r') as lyricFile:
			data = lyricFile.read().replace('\n', ' ')
	except:
		print('error')
		errors += 1
		continue

	# Remove terms of use
	data = re.sub(r"\A.+(Terms of Use)", '', data, re.DOTALL)

	# Remove copy right
	data = re.sub(r"(Song Discussions).+$", '', data, re.DOTALL)

	# Remove "no lyrics message"
	data = re.sub(r"(Hmm, that's).+('em.)", '', data, re.DOTALL)

	# Write sanitised lyric to the lyricFile
	with open(fileName, 'w') as lyricFile:
		lyricFile.write(data)

	splitData = data.split(' ')

	word_list_count = len(splitData)

	unique = len(set(splitData))

	ratio = round( (1 - (unique / word_list_count)) * 100, 3)

	# holds year,artist,album,song
	directoryCSVInfo = re.sub('[^-a-zA-Z0-9_. ]+',',', os.path.dirname(fileName))[8:]

	writeCSVData = directoryCSVInfo + ',' + str(word_list_count) + ',' + str(unique) + ',' + str(ratio) + '\n';
	
	print(writeCSVData)

	lyricDatasetCSV.write(writeCSVData)

	print(calculatedSongs)

	calculatedSongs += 1;

# End timer
elapsed_time = timer() - start
print('elapsed time = ' + str(elapsed_time))
print('calculated and recorded : ' + str(calculatedSongs))
print('errors : ' + str(errors))
lyricDatasetCSV.close()