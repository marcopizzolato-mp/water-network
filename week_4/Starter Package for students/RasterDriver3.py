from RasterHandler import createRanRasterSlope
import matplotlib.pyplot as mp
from Flow import FlowRaster

rows=10
cols=15
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

for p in fr.getPointList():
    mp.scatter(p.get_x(),p.get_y(), color='yellow')
    
    if (p.getDownnode()!=None):
        x1=p.get_x()
        y1=p.get_y()
        x2=p.getDownnode().get_x()
        y2=p.getDownnode().get_y()
        mp.plot([x1,x2],[y1,y2],color="black")

    if (p.getPitFlag()):
        mp.scatter(p.get_x(),p.get_y(),color="red")

mp.show()