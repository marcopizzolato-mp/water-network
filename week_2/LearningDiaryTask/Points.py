# -*- coding: utf-8 -*-
"""
"""

import math


class Point2D(object):
    '''A class to represent 2-D points'''

# The initialisation methods used to instantiate an instance
    def __init__(self,x,y):  
#ensure points are always reals
        self._x=x
        self._y=y
 
#return a clone of self (another identical Point object)        
    def clone(self):
        return Point2D(self._x,self._y)

#return x coordinate    
    def get_x(self):
        return self._x
        
#return y coordinate           
    def get_y(self):
        return self._y
        
#return x coord if arg=0, else y coord
    def get_coord(self,arg):
        if arg==0:
            return self._x
        else:
            return self._y
            
        
#return x,y tupel        
    def get_xys(self):
        return (self.x,self._y)        
    
    #move points by specified x-y vector
    def move(self,x_move,y_move):
        self._x = self._x + x_move
        self._y = self._y + y_move
        
#calculate and return distance    
    def distance(self, other_point):
 #     put in check to see if other point is a point
     xd=self._x-other_point._x
     yd=self._y-other_point._y
     return math.sqrt((xd*xd)+(yd*yd))
     
     
    def bearingTo(self, other_point):
		
       otherX = other_point.get_x()
       otherY = other_point.get_y()
# All geometry is in radians 
# we could convert to degrees if we wanted
# math.pi is a  funtion of the math module
       distance = self.distance(other_point)
       sinTheta = (otherX - self._x) / distance
       cosTheta = (otherY - self._y) / distance

       aSinTheta = math.asin(sinTheta)

#These conditions give an angle between 0 and 2 Pi radians
#You should test them to make sure they are correct
       if (sinTheta >= 0.0 and cosTheta >= 0.0):
           theta = aSinTheta
       elif (cosTheta < 0.0):
           theta = math.pi - aSinTheta
       else:
           theta = (2.0 * math.pi + aSinTheta)
       return theta
       
     
    def samePoint(self,point):
        if point==self:
             return True

    def sameCoords(self,point,absolute=True,tol=1e-12):
        if absolute:
            return (point.get_x()==self._x and point.get_y()==self._y)
        else:
            xequiv=math.abs((self.get_x()/point.get_x())-1.)<tol
            yequiv=math.abs((self.get_y()/point.get_y())-1.)<tol
            return xequiv and yequiv
            
    def __str__(self):
        return ('x={:.2f} y={:.2f}').format(self._x, self._y)

    
#End of calss Point 2D
#********************************************************


class PointField(object):
    '''A class to represent a field (collection) of points'''
    
    def __init__(self,PointsList=None):
        self._allPoints = []
        if isinstance(PointsList, list):
            self._allPoints = []
            for point in PointsList:
                if isinstance(point, Point2D):
                    self._allPoints.append(point.clone())
  
    def getPoints(self):
        return self._allPoints
        
    def size(self):
        return len(self._allPoints)
    
    def move(self,x_move,y_move):
        for p in self._allPoints:
            p.move(x_move,y_move)
    
    def append(self,p):
        self._allPoints.append(p.clone())

#method nearestPoint
    def nearestPoint(self,p,exclude=False):
        """A simple method to find the nearest Point to the passed Point2D
        object, p.  Exclude is a boolean we can use at some point to
        deal with what happens if p is in the point set of this object, i.e
        we can choose to ignore calculation of the nearest point if it is in 
        the same set"""
 
#check we're been passed a point   
        if isinstance(p,Point2D):
 
#set first point to be the initial nearest distance           
            nearest_p=self._allPoints[0]           
            nearest_d=p.distance(nearest_p)

# now itereate through all the other points in the PointField
# testing for each point, i.e start at index 1
            for testp in self._allPoints[1:]:

# calculate the distance to each point (as a test point)
                d=p.distance(testp)

# if the test point is closer than the existing closest, update
# the closest point and closest distance
                if d<nearest_d:
                    nearest_p=testp
                    nearest_d=d

# return the nearest point                    
            return nearest_p

#else not a Point passed, return nothing       
        else:
            return None
            
        

    def sortPoints(self):
           """ A method to sort points in x using raw position sort """
           self._allPoints.sort(pointSorterOnX)
        
        
   
class Point3D (Point2D):

    def __init__(self, x, y, z):
        print ('I am a Point3D object')
        Point2D.__init__(self, x, y)
        self._z = z
        print ('My z coordinate is ' + str(self._z))
        print ('My x coordinate is ' + str(self._x))
        print ('My x coordinate is ' + str(self._y))

    def clone(self):
        return Point3D(self._x, self._y, self._z)
        
    def get_z(self):
        return self._z
    
    def move(self, x_move, y_move, z_move):
        Point2D.move(self,x_move, y_move)
        self._z = self._z + z_move
    
    def distance(self, other_point):
        zd=self._z-other_point.get_z()
#        xd=self._x-other_point.get_x()
#        yd=self._y-other_point.get_y()
        d2=Point2D.distance(self,other_point)
        d3=math.sqrt((d2*d2)+(zd*zd))
        return d3
        

    
def pointSorterOnX(p1,p2):
    x1=p1.get_x()
    x2=p2.get_x()
    if (x1<x2): return -1
    elif (x1==x2): return 0
    else: return 1

def pointSorterOnY(p1,p2):
    y1=p1.get_y()
    y2=p2.get_y()
    if (y1<y2): return -1
    elif (y1==y2): return 0
    else: return 1


class Dpoint(Point2D):
    def __init__(self, x, y, d=None, i=None):
        Point2D.__init__(self, x, y)
        self._distance=d
        self._index=i
        
    def setD(self, d):
        self._distance=d   
    def getD(self):
        return self._distance;
    
    def setI(self, i):
        self._index=i
    def getI(self):
        return self._index