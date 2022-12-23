import numpy as np
import matplotlib.pyplot as mp
import random
from RasterHandler import readRaster

### EXTERNAL RASTER 2
# load an external rasteras object of the class "raster"
raster = readRaster("raster_test2.txt")
raster2 = raster.getData()
# get the size of the raster calling 2 methods fromthe class "Raster"
rows = raster.getRows()
cols = raster.getCols()


#rows=100 # set number of rows
#cols=100 # ser number of columns

# create a raster of zeros with dimension "rows" "cols"
data=np.zeros((rows,cols))
# loop over all the cells in the raster and assign a random value
for i in range(rows):
    for j in range(cols):
        data[i,j]=round(random.random(),2) #added: round

# print the 2D Array
print (data)

# create a second raster of zeros with the same dimension of data
focalMean=np.zeros((rows,cols))

# set the search box size
search=1
# calculate the visited cells
# no need to calculate the number of cells visited because
# we are excluding those that would have an incomplete buffer around
meanDenom=(search*2+1)*(search*2+1)
raster3 = np.zeros((rows,cols))
# on the original aster visit all the cells in a inner raster defined by the search box size "buffer"
# each reiteration the loop will focus on a specific cell of interest
for i in range(search, (rows-search)):
    for j in range(search, (cols-search)):
       # for each cell of interest in the inner raster
       # set focalsum variable to zero
       focalSum=0
       # and navigate the search progressively summing them
       for ii in range(i-search, i+search+1):
           for jj in range(j-search, j+search+1):
               focalSum=focalSum+raster2[ii,jj]   #data[ii, jj]
               
       # after visiting all the cells in the search box
       # store the average value in a cell of the focal mean raster
       #focalMean[i,j]=focalSum/meanDenom
       raster3[i,j]=focalSum/meanDenom

# display the original raster
mp.imshow(raster2, cmap='RdYlGn')
mp.colorbar()
mp.show()
 
# display the mean raster after applying the filter
mp.imshow(raster3, cmap='RdYlGn')
mp.colorbar()
mp.show()

