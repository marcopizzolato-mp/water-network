# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:04:00 2018

@author: gwatmoug
"""

########################## Binary Search 1st Example #############################

def binarySearch(alist, item):
   
    first = 0
    last = len(alist)-1
    found = False
    
    while first <=last and not found:       
        midpoint = (first + last)//2       
        if alist[midpoint]==item:
            found = True       
        else:       
            if item < alist[midpoint]:
                last = midpoint-1               
            else:
                first = midpoint+1
    return found

testlist = [0,1,2,8,13,17,19,32,42]

print('Result of First')
print(binarySearch(testlist, 5))


########################## Binary Search 2nd Example #############################

def binarySearch2(s, mylist):    
    lower = 0;
    upper = len(mylist)

    if len(mylist)==0 or not s in mylist: 
        print('Nothing to search or does not have what we want to find.')
        return -1
    while (True) and not (lower == upper):
        midpoint = (lower+upper)//2        
        print (str(lower)+ " " + str(upper) + " " + str(midpoint))       
        sm = mylist[midpoint]
        print (str(sm)) 
        
        if (sm<s):
            lower = midpoint
        elif (sm>s):
            upper = midpoint
        else:
            return midpoint


testlist = [0,1,2,8,13,17,19,32,42]

print('Result of Second')
print(binarySearch(5, testlist))


########################## Binary Search 3nd Example #############################

def binarySearch3(s, mylist):    
    lower = 0;
    upper = len(mylist)

    if len(mylist)==0: #or not s in mylist: 
        print('Nothing to search or does not have what we want to find.')
        return -1
    while (True) and not (lower == upper):
        midpoint = (lower+upper)//2        
        print (str(lower)+ " " + str(upper) + " " + str(midpoint))       
        sm = mylist[midpoint]
        print (str(sm)) 
        
        if (sm<s):
            lower = midpoint
        elif (sm>s):
            upper = midpoint
        else:
            return midpoint


testlist = [0,1,2,8,13,17,19,32,42]

print('Result of Second')
print(binarySearch(5, testlist))