import numpy as np

from Points import Point2D
# Added to fix the code
from Raster import Raster

class FlowNode(Point2D):
    
    def __init__(self,x,y, value):
        Point2D.__init__(self,x,y)
        self._downnode=None
        self._upnodes=[]
        self._pitflag=True
        self._value=value
        
    def setDownnode(self, newDownNode):
        self._pitflag=(newDownNode==None)
        
        if (self._downnode!=None): # change previous
            self._downnode._removedUpnode(self)
            
        if (newDownNode!=None):
            newDownNode._addUpnode(self)
            
        self._downnode=newDownNode 
        
    def getDownnode(self):
        return self._downnode 
        
    def getUpnodes(self):
        return self._upnodes
    
    def _removedUpnode(self, nodeToRemove):
        self._upnodes.remove(nodeToRemove)
    
    def _addUpnode(self, nodeToAdd):
        self._upnodes.append(nodeToAdd)

    def numUpnodes(self):
        return len(self._upnodes)
        
    def getPitFlag(self):
        return self._pitflag 
    
    
    def getElevation(self):
        return self._value
  
    def __str__(self):
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())
    
class FlowRaster(Raster):

    def __init__(self,araster):
        super().__init__(None,araster.getOrgs()[0],araster.getOrgs()[1],araster.getCellsize())
        data = araster.getData()
        nodes=[]
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y=(i)*self.getCellsize()+self.getOrgs()[0]
                x=(j)*self.getCellsize()+self.getOrgs()[1]
                nodes.append(FlowNode(x,y, data[i,j]))
            
        nodearray=np.array(nodes)
        nodearray.shape=data.shape
        self._data = nodearray

        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
        self.setDownCells()
        
              
    def getNeighbours(self, r, c):
        neighbours=[]
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])
                
        return neighbours
    
    def lowestNeighbour(self,r,c):
        lownode=None
        
        for neighbour in self.getNeighbours(r,c):
            if lownode==None or neighbour.getElevation() < lownode.getElevation():
                lownode=neighbour
        
        return lownode

    def setDownCells(self):
       for r in range(self.getRows()):
           for c in range(self.getCols()):
               lowestN = self.lowestNeighbour(r,c)
               if (lowestN.getElevation() < self._data[r,c].getElevation()):
                   self._data[r,c].setDownnode(lowestN)
               else:
                   self._data[r,c].setDownnode(None)
    
    def extractValues(self, extractor):
        values=[]
        for i in range(self._data.shape[0]):
            for j in range(self._data.shape[1]):
                values.append(extractor.getValue(self._data[i,j]))
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        return valuesarray
    
class FlowExtractor():
    def getValue(self, node):
        return node.getFlow()
