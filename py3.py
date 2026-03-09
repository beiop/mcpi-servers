
from pathlib import Path
#import os,subprocess
from mcpi import minecraft
from mcpi import connection

import time
import base64
from mcpi import util

#blue 1
#red 2
#green 3
#banana 4

#78 83 88 98

class Vect:
    def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
         
def ascii(input):
    print(input)
    return base64.b64decode(str(input + "=" * (-len(input) % 4))).decode("ascii")


mcB = minecraft.Minecraft.create("localhost",4707)
mcB.reborn.disableCompatMode()
entities = mcB.getEntities(-1) #get all entity types
print(entities)
if entities != []:
    for i in range(len(entities)):
        current = entities[i]
        print(entities[i])

time.sleep(1)
players = mcB.getPlayerEntityIds()
print(players)
for i in players:
     mcB.entity.setTilePos(i,-2,2,-37)

redCake = -1,0,-38
cake = 92   
air = 0
redObsidian = (-4,1,-40)

redGenerator = -1,0,-45

mcB.setBlock(redCake,cake,0)
mcB.setBlock(redGenerator,air)

count = 0
redIronStacks = []
while True:
    
    mcB.entity.spawnItem(*redGenerator,265,1)
    count += 1
    if count > 500:
        count = 0
        redObsidianIds = []
        entities = mcB.getEntities(64) #get all entity types with -1
        print(entities)
        for i in range(len(entities)):
            current = entities[i]
            
            if connection.timeoutVar == False:
                print(ascii(mcB.entity.getName(current[0])),mcB.entity.getSelectedItem(current[0]))
            else:
                print("py3.py exited a loop to re-get the list of entities")
                entities = []
                connection.timeoutVar = False
                break
        if entities != []:
            for i in range(len(entities)):
                current = entities[i]
                if (current[2],current[3],current[4]) == redObsidian:
                    redObsidianCount += 1
                    redObsidianIds.append(current[0])
                if len(redObsidianIds) >= 1:
                    for j in redObsidianIds:
                          mcB.removeEntity(i)
                    mcB.spawnEntity(*redGenerator,)


    time.sleep(0.1)


[1, 10, -40.428139, 0.0, 0.178345]
[2, 10, -40.770279, 0.0, 1.784805]
[3, 10, -41.075844, 0.0, 0.417953]
[4, 10, -39.475853, 0.0, 0.744034]
[32, 64, -1.203278, 0.0, -42.427444]
[7]
[1, 10, -38.846405, 0.0, 2.552124]
[2, 10, -43.076057, 0.0, 0.605896]
[3, 10, -41.165298, 0.0, -0.414314]
[4, 10, -42.476021, 0.0, 1.940536]
[40, 64, -1.707939, 0.0, -37.680893]
[7]
time.sleep(1)

