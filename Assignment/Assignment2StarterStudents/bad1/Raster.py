# -*- coding: utf-8 -*-
"""

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
    # returns the data in the raster - it is an array     
    def getData(self):
        return self._data

    def getData2(self):
        values=[]
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                values.append(round(self._data[r,c],2))
        return values
        
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
        ''' Methid that resamples the raster according to a resample factor
        Args: rater(self) and factor'''
        newRowNum = self.getRows() // factor
        newColNum = self.getCols() // factor
        newdata = np.zeros([newRowNum, newColNum])
           
        for i in range (newRowNum):
            for j in range (newColNum):
                sumCellValue = 0.0
                   
                for k in range (factor):
                    for l in range (factor):
                        sumCellValue += self._data[i*factor + k, j*factor + l]
                    newdata[i,j] = sumCellValue / factor / factor
                   
        return Raster(newdata, self._orgs[0], self._orgs[1], self._cellsize*factor)        
       #if factor== 1:
       #    return self
       #else:
           #raise ValueError("createWithIncreasedCellsize: not fully implemented so only works for scaling by factor 1!")


    
           
