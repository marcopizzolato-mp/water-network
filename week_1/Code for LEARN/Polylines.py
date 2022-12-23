# -*- coding: utf-8 -*-
"""

"""
from Points import Point2D

class Polyline(object):
    
    '''A class to represent 2-D points'''

# The initialisation methods used to instantiate an instance
    def __init__(self,arg=None):
      if isinstance(arg, list):
          self._allPoints = []
          for point in arg:
              if isinstance(point, Point2D):
                  self._allPoints.append(point.clone ())
      elif isinstance(arg, Point2D):
          self._allPoints = [arg.clone()]
      else:
          self._allPoints = []
      self.id=None
          
    def size(self):
        return len(self._allPoints)    
    
    def getPoint(self,i):
        return self._allPoints[i]
        
    def getPoints(self):
        return self._allPoints
        
    def getPointsAsLists(self):
        x=[]
        y=[]
        for p in self._allPoints:
            x.append(p.get_x())
            y.append(p.get_y())
        return (x,y)
        
    def setID(self,id):
        self.id=id

    def append(self,point):
        if isinstance(point, Point2D):
            self._allPoints.append(point.clone ())
        elif isinstance(point, tuple):
            self._allPoints.append(Point2D(point[0],point[1]))
            
    def insertAt(self,point,i):
        if isinstance(point, Point2D):
            self._allPoints=self._allPoints[:i]+[point.clone()]+self._allPoints[i:]
            
    def getSegment(self,i):
        if i<0 or i>len(self._allPoints)-2:
            return None
        else:
            seg=Segment(self._allPoints[i],self._allPoints[i+1])
            return seg
            
    def getSegments(self):
        if self.size()<2:
            return None
        else:
            segs=[]
            for i in range(len(self._allPoints) -1):
                segs.append(self.getSegment(i))
            return segs
            
    def closest(self,point):
        minp=self._allPoints[0]
        mind=minp.distance(point)
            
        for p in self._allPoints[1:]:
            d=p.distance(point)
            if d<mind:
                mind=d
                minp=p
            
        for seg in self.getSegments():
            p=seg.getIntersect(point)
            if not(p==None):
                d=p.distance(point)
                if d<mind:
                    mind=d
                    minp=p
        return minp
            
class Segment(object):
    
    def __init__(self,*args):
         if len(args)==4:
             p1=Point2D(args[0],args[1])
             p2=Point2D(args[2],args[3])
             self._segPoints=(p1,p2)
         elif len(args)==1:
             plist=args[0]
             p1=plist[0]
             p2=plist[1]
             self._segPoints=(p1.clone(),p2.clone())
         else:
             p1=args[0]
             p2=args[1]
             self._segPoints=(p1.clone(),p2.clone())
             
         
             
    def getStart(self):
        return self._segPoints[0]
    
    def getEnd(self):
        return self._segPoints[1]
        
    def getIntersectLine(self,point):
        x1=self.getStart().get_x()
        y1=self.getStart().get_y()
        x2=self.getEnd().get_x()
        y2=self.getEnd().get_y()
        x3=point.get_x()
        y3=point.get_y()
#        print x1,y1,x2,y2,x3,y3
        m1 = (y2-y1)/(x2-x1)
        c1 = y1-(m1*x1)
        c2 = y3+(x3/m1)
        x4 =(c2-c1)/(m1+(1./m1))
        y4=(m1*x4)+c1
        return Point2D(x4,y4)
        

    def inXRange(self,point):
        x1=self._segPoints[0].get_x()
        x2=self._segPoints[1].get_x()
        px=point.get_x()
        
        minx=min(x1,x2)
        maxx=max(x1,x2)
        
        return (px>=minx)and(px<=maxx)
        
                
    def getIntersect(self,point):
        ip=self.getIntersectLine(point)
        if self.inXRange(ip):
            return ip
        else:
            return None
            
    def getClosest(self,point):
        ip=self.getIntersectLine(point)
        if self.inXRange(ip):
            return ip
        else:
            d1=self._segPoints[0].distance(point)
            d2=self._segPoints[1].distance(point)
            if d1<d2:
                return self._segPoints[0]
            else:
                return self._segPoints[1]