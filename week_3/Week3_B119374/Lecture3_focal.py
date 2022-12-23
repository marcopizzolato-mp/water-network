import numpy as np
import matplotlib.pyplot as mp
# import random
from RasterHandler import readRaster

### EXTERNAL RASTER 2 ###
# load an external rasteras object of the class "raster"
raster = readRaster("raster_test2.txt")
data = raster.getData()
# get the size of the raster calling 2 methods fromthe class "Raster"
rows = raster.getRows()
cols = raster.getCols()

### NOT NEEDED BECAUSE IMPORTIN EXTERNAL RASTER ###

#rows=100 # set number of rows
#cols=100 # ser number of columns

# create a raster of zeros with dimension "rows" "cols"
#data=np.zeros((rows,cols))
# loop over all the cells in the raster and assign a random value
#for i in range(rows):
#    for j in range(cols):
#        data[i,j]=round(random.random(),2) #added: round

# print the 2D Array
# print (data)

### END ###


# set the search box size
search=2

# create a second raster of zeros with the same dimension of data
focalMean=np.zeros((rows-search*2,cols-search*2)) ## modified by B119374##


# calculate the visited cells
# no need to calculate the number of cells visited because
# we are excluding those that would have an incomplete buffer around
meanDenom=(search*2+1)*(search*2+1)

# on the original aster visit all the cells in a inner raster defined by the search box size "buffer"
# each reiteration the loop will focus on a specific cell of interest
for i in range(0, (rows-search*2)):         ## modified by B119374##
    for j in range(0, (cols-search*2)):     ## modified by B119374##
       # for each cell of interest in the inner raster
       # set focalsum variable to zero
       focalSum=0
       # and navigate the search progressively summing them
       for ii in range(i-search, i+search+1): 
           for jj in range(j-search, j+search+1):
               focalSum=focalSum+data[ii,jj]   #data[ii, jj]
               
       # after visiting all the cells in the search box
       # store the average value in a cell of the focal mean raster
       focalMean[i,j]=focalSum/meanDenom
       
# display the original raster
print ('\n \n Raster - Original')
mp.imshow(data, cmap='RdYlGn')
#mp.clim(0,1) 
mp.colorbar() 
mp.show()

# display the mean raster after applying the filter
print ('\n Raster - After boxcar filter')
mp.imshow(focalMean, cmap='RdYlGn')
#mp.clim(0,1)
mp.colorbar()
mp.show()

print ('\nNice colorscale in the output raster but cutting the buffer ({})'.format(search))
print ('\nThis is the size of the original raster ({}, {})'.format(rows,cols))
print ('This is the size of the resulting raster {}'.format(focalMean.shape))
print ('It is smaller than 2* buffer'.format(rows,cols))
