from RasterHandler import createRanRasterSlope
from RasterHandler import readRaster
import matplotlib.pyplot as mp
import Flow as flow

def plotstreams(flownode,colour):
    ''' Retrieve the upnodes of a point and plot the network '''
    for node in flownode.getUpnodes():
        x1=flownode.get_x()
        y1=flownode.get_y()
        x2=node.get_x()
        y2=node.get_y()
        mp.plot([x1,x2],[y1,y2],color=colour)
        if (node.numUpnodes()>0):
            plotstreams(node,colour)

def plotFlowNetwork(originalRaster, flowRaster, title="", plotLakes=True):
    ''' Plot the flow network. Args: backgrond raster, flow raster, title '''
    print ("\n\n{}".format(title))
    mp.imshow(originalRaster._data)
    mp.colorbar()
    colouri=-1
    colours=["black","red","magenta","yellow","green","cyan","white","orange","grey","brown"]

    for i in range(flowRaster.getRows()):
        for j in range(flowRaster.getCols()):
            node = flowRaster._data[i,j]
            # if the point is a pitflag it calls the plotstream
            if (node.getPitFlag()): # dealing with a pit
                mp.scatter(node.get_x(),node.get_y(), color="red")
                colouri+=1
                plotstreams(node, colours[colouri%len(colours)])
            #     
            if (plotLakes and node.getLakeDepth() > 0):
                mp.scatter(node.get_x(),node.get_y(), color="blue")

    mp.show()

def plotExtractedData(flowRaster, extractor, title=""):
    ''' args flow Raster; Extraction function '''
    print ("\n\n{}".format(title))
    mp.imshow(flowRaster.extractValues(extractor))
    mp.colorbar()
    mp.show()

def plotRaster(araster, title=""):
    ''' Plot a Raster. Args: raster, title '''
    print ("\n\n{}, shape is  {}".format(title, araster.shape))
    mp.imshow(araster)
    mp.colorbar()
    mp.show()


def calculateFlowsAndPlot(elevation, rain, resampleF):
    ###  PLOT INPUT RASTER ----
  #  plotRaster(elevation.getData(), "Original elevation (m)")
    plotRaster(rain.getData(), "Rainfall")
    resampledElevations = elevation.createWithIncreasedCellsize(resampleF) ## Ask what is this #
    
    ################# step 1 find and plot the intial network #######
    ## it is not resampled yet
    fr=flow.FlowRaster(resampledElevations)
    # plot the network between points #
    plotFlowNetwork(elevation, fr, "Network structure - before lakes", plotLakes=False)
    
    ################Step 2 ######################################
    ## SECOND arg is the extractor function
  #  plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - constant rain")
    
    ## ARRAY of flow data    
  #  print(fr.printFlow())
    
    ################# Step 3 #######################################
    #handle variable rainfall
  #  print (rain.getData2()) # returns the values of the rain raster
    ### RAIN RANDOM DATA ###
    ''' check if the data are loaded '''
    fr.addRainfall(rain.getData())
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")
  #  print(fr.printRain()) # returns the values of the rain loaded in the flowraster



    ### TEST CUMULATIVE RAIN ## OK ----
   # fr.addRainfall(rain.getData())
   # plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")       
   # print(fr.printRain())

    ## ARRAY of flow data    
   # print(fr.printFlow())

    
   ############# step 4 and step 5 #######################################
    ## handle lakes # - orig
    fr.calculateLakes() # - orig
 #   print(fr.printFlow())
    plotFlowNetwork(elevation, fr, "Network structure (i.e. watersheds) - with lakes") # - orig
    plotExtractedData(fr, flow.LakeDepthExtractor(), "Lake depth") # - orig
   
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall") # - orig
    #print(fr.printFlow())



############### see original ##################
 #   plotExtractedData(fr, flow.FlowExtractor2(), "River flow rates - variable rainfall without addition")
 #   print(fr.printFlow())
################################################# 

############# step 1 to 4 #######################################
# Create Random Raster
rows=35
cols=35
xorg=0.
yorg=0.
xp=1 #100
yp=1 #100
nodata=-999.999
cellsize=1.
levels=4
datahi=100.
datalow=0
randpercent=0.2
    
resampleFactorA = 1
# Create random Elevation Raster
elevationRasterA=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)   
# Create random Rain Raster
rainrasterA=createRanRasterSlope(rows//resampleFactorA,cols//resampleFactorA,cellsize*resampleFactorA,xorg,yorg,nodata,levels,400,1,36,4,.1)   
# calculate the 
calculateFlowsAndPlot(elevationRasterA, rainrasterA, resampleFactorA)

############# step 5 #######################################
#calculateFlowsAndPlot(readRaster('ascifiles/dem_hack.txt'), readRaster('ascifiles/rain_small_hack.txt'), 10)



