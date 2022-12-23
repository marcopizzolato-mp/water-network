# -*- coding: utf-8 -*-
"""
Spyder Editor

Binning example simple solution for binning task in lecture 3
"""
import numpy as np

aList=['A', 'B', 'A', 'A', 'B', 'C', 'A', 'B', 'C']
array=np.array(aList)
aBiggerList=aList*100
print(aBiggerList)
aBigarray=np.array(aBiggerList)
print(array)

array2D=np.reshape(array, (3,3))
array2D=np.reshape(aBigarray, (10,90))

print(array2D)

n=3

binValues=np.zeros(n)

print(binValues)

categories=['A', 'B', 'C']
rows=len(array2D)
cols=len(array2D[0])

for i in range(rows):
    for j in range(cols):
        for v in range(n):
            if array2D[i,j] == categories[v]:
                binValues[v]+=1

print(binValues)

array1D=np.reshape(array2D, (1,900))
print(array1D)

array1D.sort()
print(array1D)