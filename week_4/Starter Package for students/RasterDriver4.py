from RasterHandler import createRanRasterSlope
import matplotlib.pyplot as mp
from Flow import FlowRaster

def plotstreams(flownode,colour):
    for node in flownode.getUpnodes():
        x1=flownode.get_x()
        y1=flownode.get_y()
        x2=node.get_x()
        y2=node.get_y()
        mp.plot([x1,x2],[y1,y2],color=colour)
        if (node.numUpnodes()>0):
            plotstreams(node,colour)

rows=20
cols=30
xorg=0.
yorg=0.
xp=5
yp=5
nodata=-999.999
cellsize=1.
levels=4
datahi=100.
datalow=0
randpercent=0.2

raster=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)   

data=raster.getData()

mp.matshow(data)
mp.colorbar()

fr=FlowRaster(raster)
fr.setDownCells()

colouri=-1
colours=["black","red","magenta","yellow","green","cyan","white","orange","grey","brown"]

for p in fr.getPointList():
    if (p.getPitFlag()):
        mp.scatter(p.get_x(),p.get_y(),color="red")
        colouri+=1
        plotstreams(p, colours[colouri%len(colours)])

mp.show()