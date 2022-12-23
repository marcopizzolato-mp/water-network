# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 00:44:33 2013

@author: nrjh
"""
import numpy as np

class Raster(object):
    
    '''A class to represent 2-D Rasters'''

# Basic constuctor method
    def __init__(self,data,xorg,yorg,cellsize,nodata=-999.999):
        self._data=np.array(data)
        self._orgs=(xorg,yorg)
        self._cellsize=cellsize
        self._nodata=nodata
        
    def getData(self):
        return self._data
        
#return the shape of the data array      
    def getShape(self):
        return self._data.shape    
    
    def getRows(self):
        return self._data.shape[0]
        
    def getCols(self):
        return self._data.shape[1]
        
    def getOrgs(self):
        return self._orgs
        
    def getCellsize(self):
        return self._cellsize
    
    def getNoData(self):
        return self._nodata
        
    # returns a new Raster with cell size larger by a factor (which must be an integer)
    def createWithIncreasedCellsize(self, factor):
        if not isinstance(factor, int):
            print ("Factor must be an int")
            return None
        
        if (self.getRows() % factor != 0):
            print ("Number of rows {} not divisible by factor {}".format(self.getRows(), factor))
            return None
        if (self.getCols() % factor != 0):
            print ("Number of cols {} not divisible by factor {}".format(self.getCols(), factor))
            return None
        
        
        newRowNum = self.getRows() // factor
        newColNum = self.getCols() // factor
        newdata = np.zeros([newRowNum, newColNum])
        
        for i in range(newRowNum):
            for j in range(newColNum):
                sumCellValue = 0.0
                
                for k in range(factor):
                    for l in range(factor):
                        sumCellValue += self._data[i*factor + k, j*factor + l]
        
                newdata[i,j] = sumCellValue / factor / factor + 100
        
        return Raster(newdata, self._orgs[0], self._orgs[1], self._cellsize*factor)

    
    