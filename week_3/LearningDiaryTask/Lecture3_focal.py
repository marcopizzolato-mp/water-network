import numpy as np
import matplotlib.pyplot as mp
import random

rows=100
cols=100

data=np.zeros((rows,cols))
for i in range(rows):
    for j in range(cols):
        data[i,j]=random.random()

print (data)
focalMean=np.zeros((rows,cols))


search=2
meanDenom=(search*2+1)*(search*2+1)

for i in range(search, (rows-search)):
    for j in range(search, (cols-search)):
       focalSum=0
       for ii in range(i-search, i+search+1):
           for jj in range(j-search, j+search+1):
               focalSum=focalSum+data[ii, jj]
                   
       focalMean[i,j]=focalSum/meanDenom

mp.imshow(data, cmap='RdYlGn')
mp.clim(0,1) 
mp.colorbar() 
mp.show() 

mp.imshow(focalMean, cmap='RdYlGn')
mp.clim(0,1)
mp.colorbar()
mp.show()
