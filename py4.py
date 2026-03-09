from mcpi import minecraft
import time
from sportsRef import *
mcT = minecraft.Minecraft.create()

mcT.reborn.enableCompatMode() #only thing I know this does is force me to use ascii()
#it also changes the way mcB.getEntities(-1) works
mcT.postToChat("Api test from turfwars.py")
players = mcT.getPlayerEntityIds()
for player in players:
    pos = mcT.entity.getPos(player)
    #mcT.entity.setPos(player,pos.x,pos.y+mH,pos.z)
    mcT.entity.setVelocity(player,0,2,0)




mW = mapWidth = 10 / 2
mL = mapLength = 20 / 2 
mY = mapYLevel = -40
mH = mapHeight = 20
mO = mapOffset = 0



mcT.setBlocks(-50,-50,-50,50,50,50,air,) #REMOVE ME
time.sleep(1)

def buildMap(t = "everything"):
    
    #floors
    mcT.setBlocks(-mW,mY,-mL,mW,mY,mO-1,bricks)
    mcT.setBlocks(-mW,mY,mO,mW,mY,mL -1,lapisBlock)

    if t != "just floors":
        #side walls
        mcT.setBlocks(-mW - 1,mY,mL -1,
                      -mW - 1,mY + mH,-mL,stoneBricks)
        mcT.setBlocks(mW + 1,mY,mL-1,
                      mW + 1,mY + mH,-mL,stoneBricks)
        
        #end chunks
        mcT.setBlocks(mW + 1,mY,mL,
                    -mW - 1,mY + mH,mL+ 5,
                    stoneBricks)
        mcT.setBlocks(mW + 1,mY,-mL -1,
                    -mW - 1,mY+ mH,-mL - 6,
                    stoneBricks)

        #end carving for spawn rooms
        mcT.setBlocks(mW,mY+1,mL+ 1,
                    -mW,mY + mH,mL+ 4,
                    air)
        mcT.setBlocks(mW,mY+1,-mL -2,
                    -mW,mY+ mH,-mL - 5,
                    air)
        #doors
        mcT.setBlocks(-4,mY+1,-mL-1,
                        -2,mY + 2,-mL,air)
        mcT.setBlocks(-4,mY+1,mL,
                        -2,mY + 2,mL,air)
        mcT.setBlocks(4,mY+1,-mL-1,
                        2,mY + 2,-mL,air)
        mcT.setBlocks(4,mY+1,mL,
                        2,mY + 2,mL+1,air)

buildMap()


time.sleep(1)
while True:
    pos = mcT.entity.getPos(players[0])
    mO = pos.z
    print(pos.z)
    buildMap("just floors")
    time.sleep(0.5)