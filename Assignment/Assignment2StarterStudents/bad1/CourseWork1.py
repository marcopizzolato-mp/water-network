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
    
    # Code to output the figure with good resolution and captions
#    mp.title('In the background the DTM - Altitude in meters (m)', fontsize=9)
#    mp.suptitle('Network structure - Before lakes', fontsize=11, fontweight='bold')
#    mp.xlabel('x coord')
#    mp.ylabel('y coord')
#    mp.savefig('./Network_structure1.png', dpi=900)

    mp.show()

def plotExtractedData(flowRaster, extractor, title=""):
    ''' Plots the flow rate
    args: flow Raster, Extraction function '''
    print ("\n\n{}".format(title))
    mp.imshow(flowRaster.extractValues(extractor))
    mp.colorbar()
    # Code to output the figure with good resolution and captions
#    mp.title('constant rain of 1 mm', fontsize=9)
#    mp.title('variable rain is measured in meters (m)\nmax rain = 400 mm', fontsize=9)
#   mp.suptitle('River flow rates in meters (mm)', fontsize=11, fontweight='bold')
#    mp.suptitle('Demonstration for task 5', fontsize=11, fontweight='bold')
#    mp.xlabel('x coord')
#    mp.ylabel('y coord')
#   mp.savefig('./FlowRates_constrain1.png', dpi=900)
#   mp.savefig('./FlowRates_variable1.png', dpi=900)
#    mp.savefig('./FlowRates_task5.png', dpi=900)

#    
    mp.show()

def plotRaster(araster, title=""):
    ''' Plot a Raster. Args: raster, title '''
    print ("\n\n{}, shape is  {}".format(title, araster.shape))
    mp.imshow(araster)
    mp.colorbar()
#    mp.title('Original elevation (m)', fontsize=9)
#    mp.title('Resampled elevation (m)', fontsize=9)
#    mp.suptitle('Digital Elevation Model', fontsize=11, fontweight='bold')
#    mp.xlabel('x coord')
#    mp.ylabel('y coord')
#    mp.savefig('./OriginalDTM_task5.png', dpi=900)
#    mp.savefig('./ResampleDTM_task5.png', dpi=900)
#    mp.show()


def calculateFlowsAndPlot(elevation, rain, resampleF):
    ###  PLOT INPUT RASTER ----
#    plotRaster(elevation.getData(), "Original elevation (m)")
#    plotRaster(rain.getData(), "Rainfall")
    resampledElevations = elevation.createWithIncreasedCellsize(resampleF)
#    plotRaster(resampledElevations.getData(), "Resampled elevation (m)")
    ################# Step 1 find and plot the intial network #######
    # Create the FlowRaster
    fr=flow.FlowRaster(resampledElevations)
    # Plot the network between points #
#    plotFlowNetwork(elevation, fr, "Network structure - before lakes", plotLakes=False)
    
    ################ Step 2 ######################################
    # Plot the extrated data - the second arg is the extractor function
#    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - constant rain")
    
    # Check # Get an array of flow values    
#    print(fr.printFlow()) # returns the values of the rain loaded in the flowraster
    
    ################# Step 3 #######################################
    ### RAIN RANDOM DATA ###
    fr.addRainfall(rain.getData())
#    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")
    
    # Check # Get an array of flow values
#    print(fr.printRain()) # returns the values of the rain loaded in the flowraster

    
   ############# step 4 and step 5 #######################################
    ## handle lakes # - orig
    fr.calculateLakes() # - orig
 #   print(fr.printFlow())
    plotFlowNetwork(elevation, fr, "Network structure (i.e. watersheds) - with lakes") # - orig
    plotExtractedData(fr, flow.LakeDepthExtractor(), "Lake depth") # - orig
    
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall") # - orig
    #print(fr.printFlow())

    ### Task 5 ###
    nomi = fr.finalCell() #finds the cell with the highest value and it's coordinate
    print (type(nomi))
    print ("Result: \n{} m of rain in x={} y={}".format(nomi[0],nomi[1],nomi[2]))

############# step 1 to 4 #######################################
# Create Random Raster
rows=20
cols=20
xorg=0.
yorg=0.
xp=1 #100
yp=1 #100
nodata=-999.999
cellsize=1.
levels=4
datahi=100.
datalow=0
randpercent=0.4
    
resampleFactorA = 1
# Create random Elevation Raster
elevationRasterA=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)   
# Create random Rain Raster
rainrasterA=createRanRasterSlope(rows//resampleFactorA,cols//resampleFactorA,cellsize*resampleFactorA,xorg,yorg,nodata,levels,400,1,36,4,.1)   
# Swap the Rsters
#calculateFlowsAndPlot(elevationRasterA, rainrasterA, resampleFactorA)

############# step 5 #######################################
calculateFlowsAndPlot(readRaster('ascifiles/dem_hack.txt'), readRaster('ascifiles/rain_small_hack.txt'), 10)



