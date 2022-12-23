from RasterHandler import readRaster
from Raster import Raster
import matplotlib.pyplot as mp

raster=readRaster("ascifiles/raster_test2.txt")
#raster=readRaster("raster_test2.txt")
data=raster.getData()

print (data)
        
mp.imshow(data)
mp.colorbar()
mp.matshow(data)
mp.colorbar()

mp.show()