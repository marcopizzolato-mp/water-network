# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 20:55:17 2018

@author: Marco
"""

def sum(list):
    sum = 0
 
    # Add every number in the list.
    for i in range(0, len(list)):
        sum = sum + list[i]
 
    # Return the sum.
    return sum
 
print(sum([5,7,3,8,10]))