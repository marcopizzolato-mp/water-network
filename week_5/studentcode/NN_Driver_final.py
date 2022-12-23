# -*- coding: utf-8 -*-
"""
"""

from PointHandler import rand_PointField
from PointPlotter import PointPlotter
from Points import Point2D
from Points import PointArray
import time

nPoints=100

pp=PointPlotter()
#create a point field
pf = rand_PointField(nPoints,0.,100.,0.,yhi=100.)

#plot the random points
pp.PointFieldScatter(pf)

#get the extent of the region covered by the points
ex=pf.get_extents()
print (ex)

#use the extent to plot a red box through it
#pp.plotBox(ex,"red")

#point array for a sparse field of points
pa=PointArray(pf,20)
#create an additional point
otherp=Point2D(50.,50.)

t=time.clock()
p=pf.nearestPoint(otherp)
t=time.clock()-t
print ("Search time = "+str(t))

print (p,p.get_x(),p.get_y())
pp.PointFieldScatter(pf)
pp.plotPoint(p,'blue')
pp.plotPoint(otherp, 'red')

pp.show()

