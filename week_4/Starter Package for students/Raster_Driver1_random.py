# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:26:45 2018

@author: gwatmoug
"""

from RasterHandler import createRanRasterSlope
import matplotlib.pyplot as mp
from Flow import FlowRaster

rows=10
cols=15
xorg=0.
yorg=0.
# Set the focus - where the elevation is highest - to check if the model works well
xp=8
yp=8
nodata=-999.999
cellsize=1.
# Not sure about level
levels=4
datahi=100.
datalow=0
randpercent=0.2

raster=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)   
     
data=raster.getData()
#print (data)
mp.matshow(data)
mp.colorbar()

