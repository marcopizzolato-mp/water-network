# -*- coding: utf-8 -*-
"""
"""
from Points import Point2D
from Points import Dpoint
import math

class Polyline(object):
    
    '''A class to represent 2-D points'''

    # Initialisation methods used to instantiate an instance
    def __init__(self,arg=None):
      # Create a polyline object if Args are list or tuple 
      if isinstance(arg, list) or isinstance(arg, tuple):
          # Create the attribute self._allPoints as an empty list
          self._allPoints = []
          for point in arg:
              # Append all the items in the arg as points2D
              if isinstance(point, Point2D):
                  self._allPoints.append(point.clone ())
      # Create a polyline object with if Point2D as argument
      elif isinstance(arg, Point2D):
          self._allPoints = [arg.clone()]
      # Create an empty list
      else:
          self._allPoints = []
      self.id=None

#### TASK WEEK 2 - PART 1 #######
      
    # Method that gives the size of the polyline object
    # Returns how many points there are in the polyline object          
    def size(self):
        return len(self._allPoints)    
    
    # Method that apply the Douglas-Peuker Line Generalization
    def generalise(self, t):
             
        # Check wether or not I do have more than two points.
        # If I have only two points I do not need to run the semplification!         
        if (self.size()<3):
            ##print ('you have only two points')
            return self
        # If I have more than two points
        else:
            # We need to check which is the further point,
            # calling the method furtherFromSeg on the polyline object,
            # which identifies the further point from segment and returns it as a Dpoint instance
            dp=self.furthersFromSeg()
            # if the further point lies with the bandwith we don't need further split
            # .get is a method of the class Dpoint
            if (dp.getD()<t):
                ##print ('within tolerance {}, max dist at {}'.format(t,dp))
                # create a new segment calling the method getStartEndSeg on the polyline objet 
                # which returns a segment with start and end point
                newSeg = self.getStartEndSeg()
                ##print ('returning {}'.format(newSeg))
                # return new segment as a polyline
                return newSeg.segAsPolyline()
            
            # if the further point lies outside of the treashold 
            else:
                # split the chain in polyline object at the furthest point (dp holds the index point)
                ##print ('Splitting at {}'.format(dp))
                v=self.split(dp.getI())
                # extract the two new chains
                c1=v[0]
                c2=v[1]
                # I call the recursion on the two sub-chains 
                # the recursion will branch as many time as necessary
                c1=c1.generalise(t)
                c2=c2.generalise(t)
                # once the recursion arrives at the end it will start returning
                # merging all the pieces that are within the tolerance
                # obtaining at the end a polyline object with a chain in it 
                # the chain has ONLY the essential points to draw the final segment
                return (self.combinePolyline(c1,c2))
            
    # Method that finds the furthest point from a segment
    def furthersFromSeg(self):
        # Call method to create a segment between the start and end point of the chain (chain=list of point 2D)
        seg = self.getStartEndSeg()
        # Call method pointSegDist to calculate the distance between point and segment
        # and reiterate the method over all the points with the for - in loop 
        distList=[]
        # (!) slide 72 - I don't get "That we iterate through the points 2 to (n-1)"
        # I'm just runnign over ALL the list ! How to improuve?
        for item in self._allPoints:
            dist=seg.pointSegDist(item)
            distList.append(dist)
        
        # Storing the index of the max value
        maxIndex=distList.index(max(distList))
        # Storing the max value
        maxVal=max(distList)
        # Store the furthest point as a Point 2D element - class Dpoint
        maxPoint = Dpoint(self._allPoints[maxIndex].get_x(),self._allPoints[maxIndex].get_y(),maxVal,maxIndex)
        # Return the point1D
        return maxPoint

    
    ## method to create a subchain of a polyline splitting the polyline at "index"
    def split(self,index):
        list1a=[]
        list1b=[]
        list1a=self._allPoints[:index+1]
        list1b=self._allPoints[index:]
        # v contains two polylines
        v=[Polyline(list1a),Polyline(list1b)]
        return v
    
    ## function that creates a polyline from polylines
    def combinePolyline(self,c1,c2):
        c1Len=c1.size()
        #c2Len=c2.size
        # combine two polylines
        combo=Polyline(c1._allPoints[:c1Len-1]+c2._allPoints)
        return combo

### END - PART 1 ###
   
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

### TASK - PART 2 ###
        
## CONSTRUCT A SEGEMENT BETWEEN START AND END POINT ##    
    # Identifies the start and end point of a segment
    def getStartEndSeg(self):
        if (self.size()<2):
            return None
        else:
            return Segment(self.getStart(), self.getEnd())

    # Returns start Point of a segment
    def getStart(self):
        if (len(self._allPoints)>0):
            return self.getPoint(0)
        else:
            return None 

    # Returns end Point of a segment 
    def getEnd(self):
        if (len(self._allPoints)>0):
            return self.getPoint(self.size()-1)
        else:
            return None

### END - PART 2 ###
        
    def setID(self,id):
        self.id=id

    def addPoint(self,point):
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
    
### TASK - PART 3 ###
             
    # Transform the Segment element in a polyline element
    def segAsPolyline(self):
        items = []
        items.append(self.getStart())
        items.append(self.getEnd())
        return Polyline(items)
    


    # measure the distance between the a point and the line
    def pointSegDist(self,P1):
        # find the x and y of the segment start and end points
        x1=self._segPoints[0].get_x()
        x2=self._segPoints[1].get_x()
        y1=self._segPoints[0].get_y()
        y2=self._segPoints[1].get_y()
       
        #finds the coordinates of the point P1
        P1x=P1.get_x()
        P1y=P1.get_y()
        # math here, get the distance line - point
        xdiff = x2-x1
        ydiff = y2-y1
        num = abs(ydiff*P1x - xdiff*P1y + x2*y1 - y2*x1)
        den = math.sqrt(ydiff**2 + xdiff**2)
        return num / den

### END - PART 3 ###
             
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
    
                






			
		
			
	


         

     