import matplotlib as mpl
import numpy as np
import pylab as plt
import csv
import re
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import pandas as pd

fileName_Sample = './../lyricDataset.csv'      	
csv_Sample = pd.read_csv(fileName_Sample)
data_Sample = csv_Sample[['Year','Artist','Song','CompressedRatio']]

Y_Sample = data_Sample['CompressedRatio']

plt.xkcd()

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(True)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(True) 

# Make the grid lines
ax.xaxis.get_gridlines()
ax.xaxis.grid(linewidth=1, zorder=5)
ax.yaxis.grid(linewidth=1, zorder=5)
plt.rc('axes', axisbelow=True)
plt.grid(True, lw=2.5, alpha=0.5, zorder=0)

# Ensure that the axis ticks only show up on the bottom and left of the plot.       
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()   

# Make sure your axis ticks are large enough to be easily read.      
plt.yticks(range(0, 30001, 5000), fontsize=40)    
plt.xticks(range(0, 101, 10), [str(y) + " " for y in range(0, 101, 10)], fontsize=40)     

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on")  
 
# Avoid unnecessary whitespace.    
plt.ylim(0, 30500)    
plt.xlim(0, 101) 

plt.hist((Y_Sample), color="#3F5D7D", bins=60, zorder=2)  

plt.show()

