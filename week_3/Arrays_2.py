# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:18:15 2018

@author: Marco
"""

import numpy as np
from copy import deepcopy
import matplotlib.pyplot as mp
from RasterHandler import readRaster

'''
### PRINT AN ITEM IN THE ARRAY ###

mylist=[]
mylist2=[]
# The problem has ben solved with declaring "list" before
mylist = list(range(21,31))
mylist2 = list(range(51,61))
#Quick way to generate an array
#mylist3 = np.arange(1,11)



print ('this is my list 1 \n {}'.format(mylist))

print ('this is my list 2 \n {}'.format(mylist2))

my1Darray1=np.array(mylist)
my1Darray2=np.array(mylist2)
my2Darray1=np.array([mylist,mylist2])
print('these are my 1D arrays')
print(my1Darray1)
print(my1Darray2)

print('this is my 2D array \n {}'.format(my2Darray1))

### GET 3D arrays as combo of 2 2D arrays 
## 3D array IS A COMBINATION OF 2D arrays
## 

my2Darray2 = deepcopy(my2Darray1)

#my2Darray1=np.array([mylist,mylist2])

my3Darray1=np.array([my2Darray1,my2Darray2])
print('this is my 3D array \n {}'.format(my3Darray1))

### ACCESS THE DATA ###

#Quick way to generate an array
myArray3 = np.arange(30)
print ('this is my array3 \n {}'.format(myArray3))

b=np.reshape(myArray3, (15,2)) # reshape is a method in numpy
print ('this is b \n {}'.format(b))
print ('the shape of the array is \n {}'.format(str(b.shape)))

c=np.reshape(myArray3, (5,3,2)) # reshape is a method in numpy
print ('this is c \n {}'.format(c))
print ('the shape of the array is \n {}'.format(str(c.shape)))

d = deepcopy(c)

c.shape=(30) # reshape directly
print ('this is c \n {}'.format(c))
print ('the shape of the array is \n {}'.format(str(c.shape)))
'''

### Missing array operations

###EXTERNAL RASTER 1
#raster1 = readRaster("RasterExample1.txt")

#mp.imshow(raster1.getData(), cmap='RdYlBu')
#mp.colorbar()
#mp.show()

###EXTERNAL RASTER 2
#raster2 = readRaster("raster_test2.txt")

#mp.imshow(raster2.getData(), cmap='pink')
#mp.colorbar()
#mp.show()


### GENERATE RASTER

rows=10
cols=5

my2Darray4 = np.zeros((rows,cols))

for i in range (rows):
    for j in range (cols):
        my2Darray4[i,j]=i+j

mp.imshow(my2Darray4)
mp.colorbar()
mp.show()

##Raster Sum
'''
rastersum=0
for i in range(rows):
    for j in range(cols):
        rastersum=rastersum+my2Darray4[i,j]
print(rastersum)
'''
##Box car filter

# Create an arrays of zeros
my2Darray5 = np.zeros(my2Darray4.shape)

#data=my2Darray4.getData()

buffer=2
denominator=(buffer*2+1)*(buffer*2+1)
print('\n buffer {}'.format(buffer))
for i in range (rows):
    for j in range (cols):
        focalSum=0
        cellsvisited=0
        for ii in range (i-buffer, i+buffer+1):
            for jj in range (j-buffer, j+buffer+1):
                #check if we are within the array boundaries
                if (ii>-1 and ii<rows and jj>-1 and jj<cols):
                    focalSum=focalSum+my2Darray4[ii,jj]
                    cellsvisited=cellsvisited+1
                    
        #my2Darray5[i,j]=round((focalSum/denominator),4)
        my2Darray5[i,j]=round((focalSum/cellsvisited),4)


mp.imshow(my2Darray5)
print('\n this the oridinal Array \n {}'.format(my2Darray4))
print('\n this the Array after the filter \n {}'.format(my2Darray5))
mp.colorbar()
mp.show()











### DISAGGREGATION ###

### There are built in methods that are doing what we are trying to do


## Go through each cell of the raster


'''
my2Darray5 = np.zeros(my2Darray4.shape)
print(my2Darray5)
#data=my2Darray4.getData()
for i in range (rows):
    for j in range (cols):
        focalSum=0
        for ii in range (i-2, i+3):
            for jj in range (j-2, j+3):
                #check if we are within the array boundaries
                if (ii>-1 and ii<cols and jj>-1 and jj<cols):
                    focalSum=focalSum+my2Darray4[ii,jj]
        
        my2Darray5[i,j]=focalSum/25

mp.imshow(my2Darray5)
mp.colorbar()
mp.show()

'''




















