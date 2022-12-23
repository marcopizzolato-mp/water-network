# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 09:36:38 2018

@author: Marco
"""

    ### TASK 4 ###            
    def calculateLakes (self,rain):

        self.addRainfall(rain.getData())

        lakeDepth = 0
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                #print (pitDepth) # must be zero at this point
                pitFlag = self._data[r,c].getPitFlag()
                #print (pitFlag) # must be true and false
                if pitFlag==True:
                    #print (pitFlag) # must be true
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
        call addRain
                
                self._rain = self._rain + newrain
                
                call get flow
                
                

                    if depth < flow
                    overflow of the pit = flow - depth
                    
                    set an attribute overflow
                    set true/false about overflow
                 ''' 
        
        
        '''
        # go through all the flownodes - retrieve the pits except the ones close to the border - put them in a list
        listPits = []
        listPits2 = []
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                
                pitFlag = self._data[r,c].getPitFlag() # checking if is a pitflag
                
                if pitFlag==True and len(self.getNeighbours(r,c)) == 8 : # ok - selecting only the pits that are within the raster
                    
                    listPits.append(self._data[r,c]) # checked - it creates a list with all the inner nodes
                     
        #print (listPits)
        #for i in listPits:
        #    print (i.getElevation())
              
        
        ## ORDER THE LIST FROM BIG TO SMALL
        listPits2 = sorted(listPits, key=lambda FlowNode: FlowNode.getElevation(), reverse=True)
        #print (listPits2)
        #for i in listPits2:
        #    print (i.getElevation())        
        
        return listPits2
        '''  