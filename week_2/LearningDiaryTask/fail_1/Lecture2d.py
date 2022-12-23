from PointPlotter import PointPlotter
from ChainHandler import ChainLoader
#import Points as pt
#import Polylines as pl


xlo=0.0
xhi=1000.0
ylo=0.0
yhi=1000.0


pp=PointPlotter()
pp.set_axis(xlo, xhi, ylo, yhi)

chain=ChainLoader("Wiggle7.txt")
pp.plotPoint(chain[0]._allPoints, 'black')

pp.plotPolylines(chain[0].generalise(40.0), 'red')
pp.show()

print (chain)

#segment = pl.Polyline(chain)
#print (segment)
#test = pt.distancePointToLine()

