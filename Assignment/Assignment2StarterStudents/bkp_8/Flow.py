import numpy as np
import sys 

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
        self._pitflag=False
        self._value=value
        # add flow attribute set to one
        self._rain=0
        self._flow=0 #
        self._lakeDepth=0
        self._lakeOverflow=0
        self._overflag=False
        self._newflow=2
        # Task 4 #
        self._lakeFlag=False
        
        
        
    def setDownnode(self, newDownNode):
        ''' ensures that there are no provblems when setting a down node'''
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
    
    ############ ORIGINAL #################
    ''' adds the rain to the flownodes '''
    def getFlow(self):
        
        upnodes = self.getUpnodes()
        self._flow = self.getRain()
        # self._flow = self._flow + self.getRain() ### NOT WORKING      
        
        if upnodes == []:
            return self._flow
        else:
            #print (upnodes)
            for node in upnodes:
                self._flow = self._flow + node.getFlow() 
              
        return self._flow
  
    ############ DEPRECATED #################
    def getFlow22(self):
        ''' added cumulative rain - deprecated'''
        upnodes = self.getUpnodes()
        self._flow = self.getRain() + self.getNewFlow() ### cumulative rain added trying to get the tast 4 1st attempt
        # self._flow = self._flow + self.getRain() ### NOT WORKING      
        
        if upnodes == []:
            return self._flow
        else:
            #print (upnodes)
            for node in upnodes:
                self._flow = self._flow + node.getFlow() 
              
        return self._flow
        
        
    #########################################    
    def getFlow2(self):
        '''return the alue of the flow'''
        return self._flow
    
   ### TASK 3 ###    
    def getRain(self):
        return self._rain
 
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
   ### modified task 4 ## 
    def lowestNeighbour(self,r,c):
        # initially set the lownode to none
        lownode=None
        # loops through a list of sorrounding point2D given by getNeighbours
        for neighbour in self.getNeighbours(r,c):
            # if the 1st iteration or the Point2D assessed is lower than the actual one it changes it
            if (lownode==None or neighbour.getElevation() < lownode.getElevation()) and neighbour.getLakeFlag() == False : ### ADD HERE is NOT LAKE ####
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
        # TO ADD # Way to check the two aster are the same size
        flowdata = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                #print(self._data[r,c].getFlow2())
                flowdata.append(self._data[r,c].getFlow2())
        valuesarray=np.array(flowdata)
        valuesarray.shape=self._data.shape
        return valuesarray        
    
    ### TASK 3 ###
    def addRainfall (self,rainArray):
        ''' method to traverse the rainfall raster and load the values in self._rain '''
        assert self._data.shape == rainArray.shape
       # print (self._data.shape)
       # print (rainArray.shape)
        rainValue = 0
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                rainValue = rainArray[r,c]
                self._data[r,c].setRain(rainValue/1000) # deprecated + self._data[r,c].getRain()) # ADDED system to get cumulative rain
    
    def printRain (self):
        ''' prints the flow value for each cell '''
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
        
        ListPits = self.getPits() #list of flownodes PITS ordered from the highest to the lowest
        listLakes =[]
        
        for i in ListPits:
            if i.getLakeFlag() == False:
                i.setLakeFlag(True) # making the pit as part of a lake
                
                mylake = lake() # create instance lake
                mylake._lakeNodes.append(i) # append 1st pit
                
                r=1
                c=1
                c = int(mylake._lakeNodes[-1].get_x())
                r = int(mylake._lakeNodes[-1].get_y())
                    
                while len(self.getNeighbours(r,c)) == 8:
                # while r >= 0 or c >= 0 or r <= self.getShape[0] or c <= self.getShape[1] : #check if i'm within the boundaries
                
                    # get the coordinates of the last point in the lake
                    c = int(mylake._lakeNodes[-1].get_x())
                    r = int(mylake._lakeNodes[-1].get_y())
                   
                    mylake._lakeNodes[-1].setLakeDepth(1) # nonsara' necessario dopo
                    # trova il vivino all'ultima cella - add it to the lake
                    lastCellNeigh = self.lowestNeighbour(r,c)
                    lastCellNeigh.setLakeFlag(True)
                    mylake._lakeNodes.append(lastCellNeigh)    
                    
                    #print (c,r)
                    #print (lastCellNeigh)
                    #print (lastCellNeigh.getElevation())
                #print("HighestWall")
                #print(mylake.maxelements())
                
                highWall = mylake.maxelements()
                mylake.setHighWall(mylake._lakeNodes[highWall[-1]]) #i might get more highwalls.. in this case I'll pick the second
                                
                badHalf=[]
                goodHalf=[]                
                badHalf = mylake._lakeNodes[highWall[-1]:]
                goodHalf = mylake._lakeNodes[:highWall[-1]]
                
                for m in badHalf:
                    #print (m.getElevation())
                    m.setLakeFlag(False)
                # print ('End')    
                mylake._lakeNodes = goodHalf
                
                listLakes.append(mylake) #this is a list of lakes, not a list of nodes
                
        #-# Tested Lakes #-# appears to work
        # print (listLakes)
        #for s in listLakes:
        #    for t in s:
        #        print(t.getElevation())
        
        #CALCULATION for LAKES
        # go through each lake
        print ('check')
        for l in listLakes:
            totFlow = 0
            for k in l._lakeNodes:
                # Calculate total flow
                if k._pitflag == True:
                    #print ('This is the pitFlow')
                    #print (k.getFlow2())
                    totFlow = totFlow + k.getFlow2()
                    
                # Set Lake depth
                highWall2 = l.getHighWall()
                depth = highWall2.getElevation() - k.getElevation() 
                k.setLakeDepth(depth)
            
            l.setlakeOutFlow(totFlow)
            #print ('This is the totflow')
            #print (totFlow)
        # Extract the coordinates of the high Wall
            cc = int(l.getHighWall().get_x())
            rr = int(l.getHighWall().get_y())
            
            # if the highwall has 8 neighbours, so it's not a border
            if len(self.getNeighbours(rr,cc)) == 8:

                # get the downnode
                nextToHighWall = self.lowestNeighbour(rr,cc)
                
                # get te flow to this cell
                print ('This is the flow before')
                print (nextToHighWall._rain)             
                nextToHighWall._rain = nextToHighWall.getRain() + l.getlakeOutFlow()
                print ('This is the flow after')
                print (nextToHighWall._rain)                 
                l.setLakeDownnode(nextToHighWall)
                
                # trickery here, set the downode of the high wall as the next one
                l.getHighWall().setDownnode(nextToHighWall)


        
        
                  
    def getPits (self):
        listPits = []
        listPits2 = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                pitFlag = self._data[r,c].getPitFlag() # checking if is a pitflag
                
                if pitFlag==True and len(self.getNeighbours(r,c)) == 8 : # ok - selecting only the pits that are within the raster
                    
                    listPits.append(self._data[r,c]) # checked - it creates a list with all the inner nodes
        
        listPits2 = sorted(listPits, key=lambda FlowNode: FlowNode.getElevation(), reverse=True)
        # check elevation
        #for i in listPits2:
        #    print (i.getElevation())        
        return listPits2
                        
class lake(list):
    
    def __init__(self):    
        self._lakeNodes=[]
        self._highWall=None
        self._lakeUpnodes=[]
        self._lakeOutFlow=0
        self._lakeDownnode=None
    
    def maxelements(self):
        
        ''' Return list of position(s) of largest element '''
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
        
    def getlakeOutFlow(self):
        return self._lakeOutFlow
 
    def setlakeOutFlow(self, value):
        self._lakeOutFlow = value 

    def getLakeDownnode(self):
        return self._lakeDownnode
 
    def setLakeDownnode(self, value):
        self._lakeDownnode = value        
        
class FlowExtractor2():
    ''' missing descrition '''
    def getValue(self, node):
        return node.getFlow22()
                    
class FlowExtractor():
    ''' missing descrition '''
    def getValue(self, node):
        return node.getFlow()

### TASK 4 ###
        
class LakeDepthExtractor():
    ''' missing descrition '''
    def getValue(self, node):
        return node.getLakeDepth()


##### DUMPING SITE #####
        '''
        ### TASK 2 ###
        ## GOOD FROM OUANA ##
    def getFlow(self):
        upnodes = self.getUpnodes()
        flow = self._rain
        
        if upnodes == []:
            flow = self._rain
            #self._flow = self.getRain()
            #return self._flow
        else:
            #print (upnodes)
            for node in upnodes:
                flow =  flow + node.getFlow()
                #node._flow = node.getRain() + node.getFlow() 
            
        return flow    
            #return node._flow
      '''
    '''
    def getFlow(self):
        upnodes = self.getUpnodes()
        flowQuant = self.getRain()
        for node in upnodes:
            flowQuant = flowQuant + node.getRain()
        return flowQuant
    '''
    '''
        ### TASK 4 ###            
    def calculateLakes (self):

        lakeDepth = 0
        # go through all the folwnodes
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                
                
                #print (pitDepth) # must be zero at this point
                pitFlag = self._data[r,c].getPitFlag() # checking if is a pitflag
                lakeFlag = self._data[r,c].getLakeFlag()  # checking if is a Lake
                # need to check if it is a lake
                # check te numbers of neighbous
                
                ## print (pitFlag) # must be true and false
                if pitFlag==True and it's not a lake and has 8 neighbours:
                    
                    # print (pitFlag) # must be true ## check 
                    
                    
        
                    pitDepth = self._data[r,c].getElevation() #get the elevation of the pit
                    lowestN = self.lowestNeighbour(r,c) #get the lowest neighbour
                    lowestNeigh = lowestN.getElevation() # get the elevation of the lowest
                    lakeDepth = lowestNeigh - pitDepth # calculte lake depth
                
                    self._data[r,c].setLakeDepth(lakeDepth) # set the lake depth 
                    # print (round(self._data[r,c].getLakeDepth(),2))
        
                    # Call the flow for all the cells
                    #self._data[r,c].getFlow()
                    #print (self._data[r,c]._flow) # print the flow of all the lakes
                    
                    ## CHECK the depth agains the flow
                  #  print ('lakes depth')
                  #  print (self._data[r,c]._lakeDepth)
                  #  print ('flow')
                  #  print (self._data[r,c]._flow) #must be zero if Flow not calculated
                    
                    while self._data[r,c].getOverFlag() == False:
                        self._data[r,c].getFlow()
                        if self._data[r,c]._lakeDepth < self._data[r,c]._flow:
                            #set the overflow
                            self._data[r,c].setLakeOverflow(self._data[r,c]._flow - self._data[r,c]._lakeDepth)
                            
                            self._data[r,c].setOverFlag(True) 
                            print ('overflag')
                            print (self._data[r,c].getOverFlag())
                            #self.lowest neigh.flow = self.lowest.neighflow + overflow
                            self.lowestNeighbour(r,c).setNewFlow(self._data[r,c].getLakeOverflow())
                            #last thing add the water volume to the nearest neighbor and that's it.
                            print ('Net Overflow')
                            print (self.lowestNeighbour(r,c).getNewFlow())
                        else:
                            self.addRainfall(rain.getData())
                             #   self._data[r,c].setOverFlag(True)                        
        '''