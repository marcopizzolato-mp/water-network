# -*- coding: utf-8 -*-
"""
Spyder Editor

Binning example simple solution for binning task in lecture 3
"""
import numpy as np
from Lecture3_modal_2 import findModal

# List of data
aList=['A', 'B', 'A', 'A', 'B', 'C', 'A', 99, 99]
# Increase the lenght of the list to have more variables
aBiggerList=aList*100
#print(aBiggerList)

# create two arrays with the size of aList and aBiglist
array=np.array(aList)
aBigarray=np.array(aBiggerList)
#print(array)
#print(aBigarray)

# Reshape the array
# Why am I overwriting the array2D ???
array2D=np.reshape(array, (3,3))
array2D=np.reshape(aBigarray, (10,90))

#print(array2D)

# i need to know the number of values before start
n=4

# create an array of zeros according to how many values there are
binValues=np.zeros(n)

print('this is the bib \n {}'.format(binValues))


categories=['A', 'B', 'C','99']
# Get the size of the array
rows=len(array2D)
cols=len(array2D[0])

for i in range(rows):
    for j in range(cols):
        for v in range(n):
            if array2D[i,j] == categories[v]:
                binValues[v]+=1

print('this are the bin value \n {}'.format(binValues))

array1D=np.reshape(array2D, (1,900))
#print(array1D)
array1D.sort()
#print(array1D)

d = np.ndarray.tolist(array1D[0])
#print(d)


findModal(d)