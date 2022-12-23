import numpy as np

from Points import Point2D
### TASK 1 ###
# Import class Raster from Module Raster.py
from Raster import Raster

class FlowNode(Point2D):
    ''' FlowNode is an instance of the Point2D Class '''
    def __init__(self,x,y, value):
        Point2D.__init__(self,x,y)
        self._downnode=None
        self._upnodes=[]
        self._pitflag=False
        self._value=value
        self._rain=0
        self._flow=0 
        self._lakeDepth=0
        self._lakeFlag=False

    def __repr__(self):
        return 'x{} y{} z{}'.format(self.get_x(),self.get_y(),self.getElevation())
        
        
    def setDownnode(self, newDownNode):
        ''' ensures that there are no provblems when setting a down node'''

        self._pitflag=(newDownNode==None)
        
        if (self._downnode!=None): # change previous
            self._downnode._removedUpnode(self)
        
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
        return self.__repr__()
    
    ### TASK 2 ###
      
    def getFlow(self):
        ''' Method that adds the rain to the flownodes using a recursive process
        Arg: the array of flownodes '''
        
        upnodes = self.getUpnodes()
        self._flow = self.getRain()  
        
        if upnodes == []:
            return self._flow
        else:    
            for node in upnodes:
                self._flow = self._flow + node.getFlow() 
     
        return self._flow
     
    def getFlow2(self):
        '''Method that returns the value of the flow'''
        return self._flow
    

    def getRain(self):
        return self._rain
   
   ### TASK 3 ###
   
    def setRain(self, value):
        self._rain = value

    ### TASK 4 ###
    def setLakeDepth(self, value):
        self._lakeDepth = value
        
    def getLakeDepth(self):
        return self._lakeDepth

    def setLakeFlag(self, value):
        self._lakeFlag = value
        
    def getLakeFlag(self):
        return self._lakeFlag
        
    def setPitFlag(self, value):
        self._pitflag = value
        
    def setLakeOverflow(self, value):
        self._lakeOverflow = value
        
    def getLakeOverflow(self):
        return self._lakeOverflow
            
    def setOverFlag(self, value):
        self._overflag = value
        
    def getOverFlag(self):
        return self._overflag
                
    def setNewFlow(self, value):
        self._newflow = value

    def getNewFlow(self):
        return self._newflow
#return x,y tupel        
    def get_xys(self):
        return (self.x,self._y) 

    
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
        # loop trough raster and create a grid of flownodes
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
        self._listino=[]
        #initialize with a random lake
        # set the coordinates of the points in the sorounding box
        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
        self.setDownCells()

        
    def getNeighbours(self, r, c):
        ''' Method that get the eigh lowest neighbours '''
        neighbours=[]
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])             
        return neighbours       

    ### modified task 4 ## 
    def lowestNeighbour(self,r,c):
        ''' Method that finds the lowest neighbour '''
        # initially set the lownode to none
        lownode=None
        # loops through a list of sorrounding point2D given by getNeighbours
        for neighbour in self.getNeighbours(r,c):
            # if the 1st iteration or the Point2D assessed is lower than the actual one it changes it
            if (lownode==None or neighbour.getElevation() < lownode.getElevation()) :
                if len(self._listino) == 0 or not self._listino[-1].isLake(neighbour) :
                    
                    lownode=neighbour

        return lownode
    
    def setDownCells(self):
        ''' Look for the lowest neighbour around the cell and set the
        downnodes '''
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
                    ### Added trying to do task 4 ###
                    self._data[r,c].setPitFlag(True)
    
    def extractValues(self, extractor):
        ''' extract values from the raster according to the extractor function'''
        values=[]
        # goes through the raster
        for i in range(self._data.shape[0]): # columns
            for j in range(self._data.shape[1]): # rows
                # extracts the values of each point
                values.append(extractor.getValue(self._data[i,j]))
        # transform the values in an array and gives to it the same shape as the data
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        return valuesarray
    
    ### TASK 2 ###
    def printFlow (self):
        ''' prints the flow value for each cell '''
        
        flowdata = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                flowdata.append(self._data[r,c].getFlow2())
        valuesarray=np.array(flowdata)
        valuesarray.shape=self._data.shape
        return valuesarray        
    
    ### TASK 3 ###
    def addRainfall (self,rainArray):
        ''' Method that traverses the rainfall raster and load the values in self._rain in meters
        Args: flownode raster, aray with rain values'''
        # Ensure rain and data have the same size
        assert self._data.shape == rainArray.shape
       # print (self._data.shape)
       # print (rainArray.shape)
        rainValue = 0
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                rainValue = rainArray[r,c]
                self._data[r,c].setRain(rainValue/1000)
    
    def printRain (self):
        ''' Method that prints the flow value for each cell
        Arg: flownode raster'''
        # TO ADD # Way to check the two aster are the same size
        raindata = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                #print(self._data[r,c].getFlow2())
                raindata.append(self._data[r,c].getRain())
        valuesarray=np.array(raindata)
        valuesarray.shape=self._data.shape
        return valuesarray   
    
    ### TASK 4 ###            
    def calculateLakes (self):
        ''' Method that calculates the lakes on the DTM linking different pits in bigger water basins
        according to the topography. Arg: flownode raster
        '''
        # Create a list of pits ordered highest to lowest
        ListPits = self.getPits() #list of flownodes PITS ordered from the highest to the lowest
        # For each pit in the list
        for i in ListPits:
            # if the Pit has not been marked as lake
            if i.getLakeFlag() == False:
                # Set the attribute Lake as True
                i.setLakeFlag(True) # making the pit as part of a lake
                
                mylake = lake() # create instance of the class Lake
                self._listino.append(mylake) # add lake to a list of lakes (attrib of class FlowRaster)
                mylake._lakeNodes.append(i) # add the Pit to a list of lake nodes (attrib of class Lake)
                
                # get coordinates of the cell
                c = int(mylake._lakeNodes[-1].get_x()/self.getCellsize())
                r = int(mylake._lakeNodes[-1].get_y()/self.getCellsize())
                
                # while both the cell is not at the margin at is a pit keep looping (while loop)
                while not ( ( len(self.getNeighbours(int(mylake._lakeNodes[-1].get_y()/self.getCellsize()),int(mylake._lakeNodes[-1].get_x()/self.getCellsize()))) < 8) and (mylake._lakeNodes[-1].getPitFlag() == True)):
                    
                    lownode2 = None # set lownode as none
                    for mm in mylake._lakeNodes: # go over all the flownodes part of the lake
                                
                        # get the coordinates of the flownode in the lake
                        c = int(mm.get_x()/self.getCellsize())
                        r = int(mm.get_y()/self.getCellsize())
                        
                        # fin the lowest neighbour to the cell
                        # ! lowestNeighbour method has been modified
                        lastCellNeigh = self.lowestNeighbour(r,c)

                        # memorize the lowest neighbour
                        if (lownode2==None or (lastCellNeigh != None and lastCellNeigh.getElevation() < lownode2.getElevation())):
                            lownode2=lastCellNeigh
                    
                    
                    lownode2.setLakeFlag(True) # Set the Flag True for the lowest
                    mylake._lakeNodes[-1].setLakeDepth(1) # Set the depth to one
                    mylake._lakeNodes.append(lownode2) # Apend the cell to the list    
                    
                # Get the high wall after the lake    
                highWall = mylake.explicit()
            
                # create two lists to split the lake according to the high wall
                badHalf=[]
                goodHalf=[]                
                
                badHalf = mylake._lakeNodes[highWall[-1]+1:] # select bad half after high wall

                goodHalf = mylake._lakeNodes[:highWall[-1]+1] # select good half before high wall
                
                # High wall included in the good half
                # un-lake the badhalf setting attribute Lake to false
                for m in badHalf:
                    
                    m.setLakeFlag(False)
                    m.setLakeDepth(0)
                
                # keep only the nodes before the high wall included 
                mylake._lakeNodes = goodHalf

                # Set the attributes down node and high wall
                if len(badHalf) > 0:
                    mylake.setLakeDownnode(badHalf[0])
                    mylake.setHighWall(goodHalf[-1])                  
                
                # append the lake to a list 
                self._listino.append(mylake) #this is a list of lakes, not a list of nodes
        
        # do over each element in the list of lakes
        for l in self._listino:
            # Go over the cells in each lake 
            for k in l._lakeNodes:
                
                # Set Lake depth
                if l.getHighWall() != None:
                    depth = l.getHighWall().getElevation() - k.getElevation() 
                    k.setLakeDepth(depth)
                
                # Set the new downNode
                k.setDownnode(l.getLakeDownnode())

            
                  
    def getPits (self):
        ''' Method to order the pits from the highest one (in altitude) to the lowest
        Arg: flownodes raster'''
        listPits = []
        listPits2 = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                pitFlag = self._data[r,c].getPitFlag() # checking if is a pitflag
                
                if pitFlag==True and len(self.getNeighbours(r,c)) == 8 : # ok - selecting only the pits that are within the raster
                    
                    listPits.append(self._data[r,c]) # checked - it creates a list with all the inner nodes
        
        listPits2 = sorted(listPits, key=lambda FlowNode: FlowNode.getElevation(), reverse=True)
        return listPits2

    ### TASK 5 ###

    def finalCell (self):
        ''' Method that returns the Max flow and the position of the cell
        Arg: flownode raster'''
        
        listPits = self.getPits2() #list of flownodes PITS ordered from the highest to the lowest
        
        lastPit = round(listPits[-1].getFlow2(),2) # get the flow
        cellCoordX = listPits[-1].get_x() # get the coordinates
        cellCoordY = listPits[-1].get_y() # get the coordinates
        
        return lastPit,cellCoordX,cellCoordY
        #print ("\n{} m of rain in x={} y={}".format(lastPit,cellCoordX,cellCoordY))

    def getPits2 (self):
        ''' Method that identifies the pits on the boundary and return a list
        Arg: flownode raster'''
        listPits3 = []
        listPits4 = []
        
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                pitFlag = self._data[r,c].getPitFlag() # checking if is a pitflag
                
                if pitFlag==True and len(self.getNeighbours(r,c)) < 8 : # ok - selecting only the pits that are on the border
                    
                    listPits3.append(self._data[r,c]) # creates a list with all the outer nodes
        
        # sort the list with an inbuilt function
        listPits4 = sorted(listPits3, key=lambda FlowNode: FlowNode.getFlow2(), reverse=False)
        
        return listPits4
    
    ### END TASK 5 ###
    
    ### TASK 4 ###
                        
class lake(list):
    
    def __init__(self):    
        self._lakeNodes=[]
        self._highWall=None # last cell belonging to the lake
        self._lakeUpnodes=[]
        self._lakeDownnode=None 

    def explicit(self):
        ''' Method that return list of position(s) of largest element '''        
        seq = []
        listin=[]
        for n in self._lakeNodes:
            seq.append(n.getElevation())
        max_val = max(seq)
        max_idx = seq.index(max_val)
        listin.append(max_idx)
        return listin
        
    def maxelements(self):
        ''' Method that return list of position(s) of largest element '''
        max_indices = []
        seq = []
        for n in self._lakeNodes:
            seq.append(n.getElevation())
        if seq:
            max_val = seq[0]
            for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
                if val == max_val:
                    max_indices.append(i)
                else:
                    max_val = val
                    max_indices = [i]
    
        return max_indices
    
    def splitLakeNodes(self,index):
        begin=[]
        end=[]
        begin=self._allPoints[:index]
        end=self._allPoints[index:]
        # v contains two polylines
        #v=[Polyline(list1a),Polyline(list1b)]
        return begin,end
    
    def getHighWall(self):
        return self._highWall
 
    def setHighWall(self, value):
        self._highWall = value
        
    def getLakeDownnode(self):
        return self._lakeDownnode
 
    def setLakeDownnode(self, value):
        self._lakeDownnode = value        

    def isLake(self, node):
        return node in self._lakeNodes
                    
class FlowExtractor():
    
    def getValue(self, node):
        ''' Method that extract the flow value from a specific node
        Args: Array of flownodes, the node of interest'''
        return node.getFlow()

    ### TASK 4 ###
        
class LakeDepthExtractor():
    def getValue(self, node):
        return node.getLakeDepth()


