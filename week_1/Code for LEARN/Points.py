# -*- coding: utf-8 -*-
"""

"""

import math

class Point2D(object):
    '''A class to represent 2-D points'''

# The initialisation methods used to instantiate an instance
    def __init__(self,x,y):  
#ensure points are always reals
        self._x=x*1.
        self._y=y*1.
        
#return a clone of self (another identical Point object)        
    def clone(self):
        return Point2D(self._x,self._y)

#return x coordinate    
    def get_x(self):
        return self._x
        
#return y coordinate           
    def get_y(self):
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
     
        
        
    def samePoint(self,point):
        if point==self:
             return True

    def sameCoords(self,point,absolute=True,tol=1e-10):
        if absolute:
            return (point.x==self._x and point.y==self._y)
        else:
            return (point._x-self._x<(point.x*tol) and point._y-self._y<(point.x*tol))
    
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
        

    
def keyFunctionOnX(p):
    return p.get_x()


def keyFunctionOnY(p):
    return p.get_y()


        
