import numpy as np

from Points import Point2D
# Added to fix the code
from Raster import Raster

class FlowNode(Point2D):
    ''' FlowNode is an instance of the Point2D Class '''
    # in addition to the x and y it can also store a value
    def __init__(self,x,y, value):
        Point2D.__init__(self,x,y)
        self._downnode=None
        self._upnodes=[] # LIST of poit2ds
        self._pitflag=True
        self._value=value
        # add flow attribute set to one
        self._rain=1
        
    # STILL OBSCURE
    # it ensure there are no problems when setting a new downnode
    def setDownnode(self, newDownNode):
        # If the newNode is none set PitFlag as True
        # If the newNode is False set the pitFlag accordingly
        self._pitflag=(newDownNode==None)
        
        # uncertain comment - check if there is something in self._downnode
        # uncertain comment - if I don't have anything in the downnode
        if (self._downnode!=None): # change previous
            # 
            self._downnode._removedUpnode(self)
        
        # uncertain comment - if new downnode is none I add upnode
        if (newDownNode!=None):
            newDownNode._addUpnode(self)
            
        self._downnode=newDownNode 
    
    # return the downnode    
    def getDownnode(self):
        return self._downnode 
    # return the upnode    
    def getUpnodes(self):
        return self._upnodes
    # remove one upnode - I need ot specify which node
    def _removedUpnode(self, nodeToRemove):
        self._upnodes.remove(nodeToRemove)
    # add an upnode - append to list
    def _addUpnode(self, nodeToAdd):
        self._upnodes.append(nodeToAdd)
    # number of upnodes
    def numUpnodes(self):
        return len(self._upnodes)
    # Returns True or False according of the pitflag is true or false     
    def getPitFlag(self):
        return self._pitflag 
    
    # Get the other atribute, which in this case is elevation 
    def getElevation(self):
        return self._value
    # print the coordinate of itself 
    def __str__(self):
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())
    ### TASK 2 ###
    def getFlow(self):
        upnodes = self.getUpnodes()
        flowQuant = self.getRain()
        for node in upnodes:
            flowQuant = flowQuant + node.getRain()
        return flowQuant

    def getRain(self):
        return self._rain
    
    ### TASK 3 ###
    def setRain(self, value):
        self._rain = value


        
        


    
class FlowRaster(Raster):
    ''' It creates a raster grid of flow nodes
        Raster stores the values as ARRAY of values
        FlowRastes stores the values as ARRAY of Point2D with elevation data '''
    def __init__(self,araster):
        # inherit the carachteristics of the parent class Raster
        super().__init__(None,araster.getOrgs()[0],araster.getOrgs()[1],araster.getCellsize())
        # extract the data from a Raster as an ARRAY (see Raster.py)
        data = araster.getData()
        # set node as empty list
        nodes=[]
        # get the dimention of the raster
        # .shape -> (row,col) -> (i,j)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y=(i)*self.getCellsize()+self.getOrgs()[0]
                x=(j)*self.getCellsize()+self.getOrgs()[1]
                nodes.append(FlowNode(x,y, data[i,j]))
        
        # array of points2D with elevation
        nodearray=np.array(nodes)
        # gives the nodearray the same shape as the origin raster and load self._data with nodearray
        nodearray.shape=data.shape
        self._data = nodearray
        
        # set the coordinates of the points in the sorounding box
        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
        self.setDownCells()
        
              
    def getNeighbours(self, r, c):
        neighbours=[]
        # loop through all the rows of neighbourIterator giving the x and y
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            # checks the boundaries
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])
        # returns a list of point2D around the central point        
        return neighbours
    
    def lowestNeighbour(self,r,c):
        # initially set the lownode to none
        lownode=None
        # loops through a list of sorrounding point2D given by getNeighbours
        for neighbour in self.getNeighbours(r,c):
            # if the 1st iteration or the Point2D assessed is lower than the actual one it changes it
            if lownode==None or neighbour.getElevation() < lownode.getElevation():
                lownode=neighbour
        # return the lowest point 2D around the cell
        return lownode
    
    # 
    def setDownCells(self):
        # Loop through the raster of Point2D 
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                # Get the lowest neighbour
                lowestN = self.lowestNeighbour(r,c)
                # if its elevation is LOWER than the one of the center cell
                if (lowestN.getElevation() < self._data[r,c].getElevation()):
                    # Set the DownNode of that Point2D as the lowestN
                    self._data[r,c].setDownnode(lowestN)
                else:
                    # if the center cell is a Pitflag than DownNode is NONE
                    self._data[r,c].setDownnode(None)
    
    def extractValues(self, extractor):
        values=[]
        # goes through the raster
        for i in range(self._data.shape[0]): # columns
            for j in range(self._data.shape[1]): # rows
                # extracts the values of each point
                ### WHERE is GET VALUE ???
                values.append(extractor.getValue(self._data[i,j]))
        # transform the values in an array and gives to it the same shape as the data
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        return valuesarray
    ### TASK 3 ###
    def addRainfall (self,rainArray):
        ''' method to traverse the rainfall raster and load the values in self._rain '''
        # missing to check if they are the same size
        rainValue = 0
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                rainValue = rainArray[r,c]
                self._data[r,c].setRain(rainValue)
       
                

    
class FlowExtractor():
    ''' missing descrition '''
    def getValue(self, node):
        return node.getFlow()
