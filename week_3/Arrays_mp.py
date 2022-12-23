# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:18:15 2018

@author: Marco
"""

import numpy as np
#from Raster import Raster
#from copy import deepcopy
import matplotlib.pyplot as mp
from RasterHandler import readRaster


### EXTERNAL RASTER 2
# load an external rasteras object of the class "raster"
raster = readRaster("raster_test2.txt")
raster2 = raster.getData()
# get the size of the raster calling 2 methods fromthe class "Raster"
rows = raster.getRows()
cols = raster.getCols()

### APPLY BOXCAR FILTER ###

# create an empty raster of zeros using a method from "Raster"
raster3 = np.zeros(raster.getShape())

# decide the buffer and print it
buffer=20
print('\n buffer {}'.format(buffer))
print('\n it takes a while...not sure why, please wait')
# per each  cell in the raster of origin
for i in range (rows):
    for j in range (cols):
        # set the variables to zero
        focalSum=0
        cellsvisited=0
        # visit all the cells in the boxcar filter 
        for ii in range (i-buffer, i+buffer+1):
            for jj in range (j-buffer, j+buffer+1):
                # check if we are within the array boundaries
                # if we don't do this python will give an error
                # because it will be searching cells that are outside of the range
                if (ii>-1 and ii<rows and jj>-1 and jj<cols):
                    # cumulative summ of the values within the search box
                    focalSum=focalSum+raster2[ii,jj]
                    # the "cellsvisited" variable provides a dynamic denominator
                    # necessary for the zones of the original raster close to the boundaries
                    # where the boxcar filter size is not complete
                    cellsvisited=cellsvisited+1
                    
        # calculates the average value and 
        raster3[i,j]=round((focalSum/cellsvisited),4)

# display the raster calling a method of the class "Raster"
mp.imshow(raster2, cmap='pink')
mp.colorbar()
mp.show()

# display the raster calling a method of the class "Raster"
mp.imshow(raster3, cmap='pink')
mp.colorbar()
mp.show()




















