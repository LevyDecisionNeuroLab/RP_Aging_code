from psychopy import core, data
import random, datetime, time
import sys, itertools
import os
import numpy as np

#delay = list(itertools.repeat(1,8))+list(itertools.repeat(2,8))+list(itertools.repeat(3,8))
#random.shuffle(delay)
#print(delay)
#orderList = list(range(1,25,1))
#random.shuffle(orderList)

def randomizeOrder(numTrials):
    outcomeA = []
    outcomeB = []
    outcomeC = []
    outcomeD = []
    
    # create a list of 1-24 (or whatever number you want, but must be the mutiple of 12)
    orderList = list(range(1,int(numTrials+1)))
    # define number of outcomes allowed for each trial type within one block, should be 2 here
    outcomeBlock = int(len(orderList)/12)
    # divide the list by 4, find out what is the max number of each segment
    x = 0.25
    maxList = []
    for m in range(4):
        maxList.append(int(len(orderList)*x))
        x+=0.25
    # define reward index
    rList1 = list(range(1,len(orderList)-4,6))
    rList2 = list(range(2,len(orderList)-3,6))
    rewardList = rList1+rList2
    # Two rules: 1) No more than two consecutive trials from the same type; 2) There must be two outcome trials from every type
    uniqueTrial = False # if ther is more than two consequitive trials from the same type
    equalOutcome = False # if this block has 2 outcome from each trial type
    while uniqueTrial == False or equalOutcome == False :
        # shuffle the 24 number list
        random.shuffle(orderList)
        # loop through the shuffled list to check for rule No.1
        r = 0
        u = []
        while r+1 < len(orderList):
            previous = orderList[r] #check 1st to 23rd number
            later = orderList[r+1] # check 2nd to 24th number
            p = []
            l = []
            for y in maxList: # find out which type the trial comes from
                if previous <= y:  # for the previous number
                    p.append(y)
                if later <= y:  # for the later number 
                    l.append(y)
            if len(p) == len(l): # if previous and later are from the same type, length will be the same
                u.append(1) # 1 - there is a repeated type
            else:
                u.append(0) # 0 - not repeated
            r += 1
        if sum(u) > 2:  # Correction - no more than two trials in a row come from the same type
            uniqueTrial = False
        else:
            uniqueTrial = True
            # Divide index numbers into four types and define outcome trials
            typeA = orderList[0:maxList[0]]
            outcomeA = list(set(rewardList)&set(typeA))
            typeB = orderList[maxList[0]:maxList[1]]
            outcomeB = list(set(rewardList)&set(typeB))
            typeC = orderList[maxList[1]:maxList[2]]
            outcomeC = list(set(rewardList)&set(typeC))
            typeD = orderList[maxList[2]:maxList[3]]
            outcomeD = list(set(rewardList)&set(typeD))
            if len(outcomeA) != outcomeBlock or len(outcomeB) != outcomeBlock or len(outcomeC) != outcomeBlock or len(outcomeD) != outcomeBlock:
                equalOutcome = False
            else:
                equalOutcome = True
    return {'typeA': typeA, 'outcomeA': outcomeA, 'typeB': typeB, 'outcomeB': outcomeB, 'typeC': typeC, 'outcomeC': outcomeC, 'typeD': typeD, 'outcomeD': outcomeD}



