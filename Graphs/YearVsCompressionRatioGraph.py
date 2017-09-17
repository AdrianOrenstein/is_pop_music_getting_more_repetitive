import matplotlib as mpl
import numpy as np
import pylab as plt
import csv
import re
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import pandas as pd

fileName_Top100 = 'lyricDatasetCSVtop100.csv'      	
csv_Top100 = pd.read_csv(fileName_Top100)
data_Top100 = csv_Top100[['Year','Artist','Song','CompressedRatio']]

fileName_WholeSample = '../lyricDataset.csv'      	
csv_WholeSample = pd.read_csv(fileName_WholeSample)
data_WholeSample = csv_WholeSample[['Year','Artist','Song','CompressedRatio']]

X = data_Top100['Year']
Y = data_Top100['CompressedRatio']
X2 = data_WholeSample['Year']
Y2 = data_WholeSample['CompressedRatio']

total_bins = 35

# Mean for Top100
bins = np.linspace(float(X.min()), float(X.max()), total_bins)
delta = bins[1]-bins[0]
idx  = np.digitize(X,bins)
running_mean = [np.mean(Y[idx==k]) for k in range(total_bins)]

# Mean for WholeSample
bins2 = np.linspace(float(X2.min()), float(X2.max()), total_bins)
delta2 = bins2[1]-bins2[0]
idx2  = np.digitize(X2,bins2)
running_mean2 = [np.mean(Y2[idx2==k]) for k in range(total_bins)]

plt.xkcd()

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

# Ensure that the axis ticks only show up on the bottom and left of the plot.      
ax.xaxis.get_gridlines()
ax.get_xticks()
ax.set_xticks([20,50,80])
ax.set_yticks([-20,-10,0])
ax.xaxis.get_gridlines()
ax.xaxis.grid(linewidth=1)
ax.yaxis.grid(linewidth=1)

# Make sure your axis ticks are large enough to be easily read.    
plt.yticks(range(40, 81, 10), [str(x) + " " for x in range(40, 81, 10)], fontsize=40)    
plt.xticks(range(1965, 2016, 10), [str(y) for y in range(1965, 2016, 10)], fontsize=40)     

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on")  

# Avoid unnecessary whitespace.    
plt.ylim(39, 81)    
plt.xlim(1964, 2016) 

plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#ffffff"

plt.grid(True, lw=2.5, alpha=0.5, zorder=0)

plt.plot(bins,running_mean,'red', lw=4, alpha=.8, zorder=2)
plt.plot(bins2,running_mean2,'blue', lw=4, alpha=.8, zorder=2)

plt.tight_layout()
plt.show()

