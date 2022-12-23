# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 18:42:07 2018

@author: Marco
"""

import numpy as np

# List of data
aList=['A', 'B', 'A', 'A', 'B', 'C', 'A', 'B', 'C']
# Increase the lenght of the list to have more variables
aBiggerList=aList*10
#print(aBiggerList)

# create two arrays with the size of aList and aBiglist
array=np.array(aList)
aBigarray=np.array(aBiggerList)
#print(array)
#print(aBigarray)

# Reshape the array
array2D=np.reshape(array, (3,3))
array2D=np.reshape(aBigarray, (1,90))

print(array2D)

print(len(array2D))
print(len(array2D[0]))