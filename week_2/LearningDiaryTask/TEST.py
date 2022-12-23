from PointPlotter import PointPlotter
from ChainHandler import ChainLoader
import Polylines as pl
import Points as pt
from copy import deepcopy

xlo=0.0
xhi=1000.0
ylo=0.0
yhi=1000.0


pp=PointPlotter()
pp.set_axis(xlo, xhi, ylo, yhi)

chain=ChainLoader("Wiggle5.txt")
pp.plotPoint(chain[0]._allPoints, 'black')

pp.plotPolylines(chain[0].generalise(20), 'red')


#seg3 = chain[0].getStartEndSeg()
#pp.plotSegment(seg3,'red')

Dlist = chain[0].furthersFromSeg()
#print('X{}  Y{}'.format(Dlist._x,Dlist._y))
#print('dist{} index{}'.format(Dlist.getD(),Dlist.getI()))
pp.plotPoint(Dlist,'cyan')


pp.show()


'''


P1 = pt.Point2D(1,1)
P2 = pt.Point2D(100,100)
P3 = pt.Point2D(800,200)
totPoints = [P1,P2,P3]
#pp.plotPoint(totPoints, 'red')
# seg = pl.Segment(totPoints)
#a = seg.getStartEndSeg()
#print(a)
#print('{}'.format(seg))

## creating a segment from a list of 3 points, and getting the distnace out
totPoints2 = pl.Polyline(totPoints)
seg = totPoints2.getStartEndSeg()
print (type(seg))
print ('{}'.format(seg.getStart()))
print ('{}'.format(seg.getEnd()))
pp.plotSegment(seg, 'red')
seg2 = pl.Segment(P1,P3)
dist = seg2.pointSegDist(P2)
print ('{}'.format(dist))



#listone=[]
#listone=totPoints2._allPoints
index=1
list1a=[]
list1b=[]
list1a=totPoints2._allPoints[:index+1]
list1b=totPoints2._allPoints[index:]
v=[pl.Polyline(list1a),pl.Polyline(list1b)]
print(v)
print(v[0])
print(v[1])

v2a=v[0]
v2b=v[1]
list2a=[]
list2b=[]
listone=(v2a._allPoints[:1]+v2b._allPoints)
print(listone)

'''