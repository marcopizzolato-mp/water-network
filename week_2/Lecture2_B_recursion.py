# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:20:37 2018

@author: gwatmoug
"""

import random
import string

def binarySearch(s, mylist):    
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

def bSearch(key, mylist, left, right):
    if (left >= right):
        return -1
    mid = (left+right)//2
    sm = mylist[mid]
    print ('search now centred at:{} '.format(sm))
    
    if (sm < key):
        print ("  moving search to right")
        return bSearch(key, mylist, mid+1, right)
    elif (sm > key):
        print ("  moving search to left")
        return bSearch(key, mylist, left, mid)
    else:
        return mid

testlist = [0,1,2,8,13,17,19,32,42]

print('Result bSerach')
print(bSearch(2, testlist,0,6))

### RANDOM GENERATOR ###

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

longl=[]
num = 6
for p in range(num):
    longl.append(id_generator())
    #print (longl[p])
for item in longl:
    print('sorted list 1' + item)
n=random.randint(0,num)

longl.sort()
print('sorted list' + str(longl))
print('search for' + longl[n])

found=binarySearch(longl[n],longl)
if (found==-1):
    print('String not found')
else:
    print('String found at position:' + str(found))

