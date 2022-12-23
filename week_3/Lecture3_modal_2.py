# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:38:53 2018

@author: gwatmoug
"""


def findModal(data):
    counts={} #dictionary not list    
    for item in data: 
        if item in counts:  #if the item is in the dictionary, add 1 to the value
            counts[item] += 1
        else: 
            counts[item] = 1 #if not in the dictionary make a new space and start at 1
       

    print ("counts={}".format(counts))  
    
    modalCount=0 
    modalVal=None 
    for key,count in counts.items(): 
        if count>modalCount:
            modalVal=key
            modalCount=count
    
    print ("modalCount={}, modalVal={}".format(modalCount, modalVal))  
 



LandUse = ['Agri', 'Agri', 'Agri', 'Grass', 'Urban', 'Woody', 'Agri', 'Woody', 'Shrub', 
           'Agri', 'Grass', 'Barren', 'Woody', 0]

findModal(LandUse)
