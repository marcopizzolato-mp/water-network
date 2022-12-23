from PointHandler import rand_PointField
from PointPlotter import PointPlotter
import time

def displayPointField(pointPlotter, pointField):
    pointPlotter.PointFieldScatter(pointField,"red")

    pl=pointField.getPoints()

    for i in range(len(pl)-1): 
        pointPlotter.plotVector(pl[i], pl[i+1],"yellow")
    
    pointPlotter.show()
 
  
xlo=0.0
xhi=1000.0
ylo=0.0
yhi=1000.0
num=20

print ("Point sorting")

pf=rand_PointField(num, xlo, xhi, ylo, yhi)
pp=PointPlotter()
pp.set_axis(xlo, xhi, ylo, yhi)

displayPointField(pp, pf)

t=time.clock()
pf.sortPoints()
t=time.clock()-t

print ("Sorting {} took {}".format(num, t))
displayPointField(pp, pf)

