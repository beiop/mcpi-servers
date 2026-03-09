#garbage collection script. 
'''
not that it's actually real garbage collection. I just will periodically check for items in a world that are in the same spot and conbine them into stacks of 64...#script that operates all the shops in sports.py
'''
from pathlib import Path
#import os,subprocess
from mcpi import minecraft
from sportsRef import *
import time
import base64
from math import floor


global clock_start, wait_time_old, wait_time
clock_start = time.clock_gettime(6)
wait_time_old = 0.0

def wait(t):
    global wait_time_old
    waited = 0
    wait_time = wait_time_old + t
    #print((clock_start + wait_time) - time.clock_gettime(6))
    while (time.clock_gettime(6)<clock_start + wait_time):
        waited += 1
        time.sleep(0.01)
    print(waited)
    wait_time_old = wait_time

mcB = minecraft.Minecraft.create("localhost",4707)

mcB.postToChat("Api test from garbagetime.py")
mcB.reborn.disableCompatMode() #only thing I know this does is force me to use ascii()
#it also changes the way mcB.getEntities(-1) works
wait(1)

items = mcB.getEntities(64)

mcB.entity.spawnItem(redGenerator,)

dictionaryWithoutACoolName = dict()
#print(items)
for item in items:
    itemInfo = str(mcB.entity.getSelectedItem(item)).split(",")
    #itemInfo[0] is the type of item
    #itenInfo[1] is the quantity
    print(itemInfo[0])
    if int(itemInfo[0]) == ironIngot:
        print(item[0])
        #{rounded location,number of items there}
        pos = (floor(item[2])+0.5,item[3],floor(item[4])+.5)
        try:
            offset = 0
            while (dictionaryWithoutACoolName[(pos[0],pos[1]+offset,pos[2])] + int(itemInfo[1])>64): # while spot is full
                offset += 0.01
            dictionaryWithoutACoolName[(pos[0],pos[1]+offset,pos[2])] += int(itemInfo[1])

        except:
            dictionaryWithoutACoolName[pos] = int(itemInfo[1])
        mcB.removeEntity(item[0])
#print(dictionaryWithoutACoolName)
for key in dictionaryWithoutACoolName.keys():
    print (key[0],key[1],key[2],itemInfo[0],dictionaryWithoutACoolName[key])
    
    mcB.entity.spawnItem(key[0],key[1],key[2],itemInfo[0],dictionaryWithoutACoolName[key])

