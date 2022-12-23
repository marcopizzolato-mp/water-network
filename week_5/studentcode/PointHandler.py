# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 17:26:35 2012
@author: nrjh
"""
from Points import Point2D
from Points import PointField
import random

def rand_PointField(number_points,xlo=0.,xhi=1.,ylo=0.,yhi=1.):
    """ Generates a point field from random points, for
    a specified number of points and x-y range specified
    as paramters"""
    newPoints=[]
    
#use xrange to generate the number of points in this set    
    for i in range(number_points):
#random numbers generated in a specific range
        x=random.uniform(xlo,xhi)
        y=random.uniform(ylo,yhi)
#add point to list
        newPoints.append(Point2D(x,y))
    
    return PointField(newPoints)
    
def rand_Point(xlo=0.,xhi=1.,ylo=0.,yhi=1.):
    """ Generates random point, for
    a specified number of points and x-y range specified
    as parameters"""

#random numbers generated in a specific range
    x=random.uniform(xlo,xhi)
    y=random.uniform(ylo,yhi)
 
    return Point2D(x,y)
    

def getPointField_fromFile(fileName):
    """ Generates a Point field (passed as string) from and x-y file
    assuming first line is a header line"""
    points = []
    myFile=open(fileName,'r')
    
#read first lien    
    myFile.readline()

#iterate through other lines
    for line in myFile.readlines():
        items=line.split('\t')
        x=float(items[0])
        y=float(items[1])
        
#generate and append new point to list        
        p=Point2D(x,y)
        points.append(p)
        
    return PointField(points)
#end of function readPoints    
    

        
#ensuere points are always re