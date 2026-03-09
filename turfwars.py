
'''
turfwars.py
starts & operates the turfwars server.


Game Loop:
    30 seconds of building start
    1 minute of fighting
        every 2 seconds, an arrow, max of 2, except Idk how to account for dropped ones unless I just delete them
        Though I'm thinking I can keep track of their thrown ones and only restock once every 2 seconds a max of two.
    15 seconds build time, or just another length of build time.
    rinse, repeat

Kit system:
    could have one 
    I'm thinking maybe each team gets 1 of each special item, and you can use it whenever you want in the game.


    
Blue is positibe on the map / playerTeams(player) == 0
red is negative on the map / playerTeams(player) == 1 

^ look up

blue is length -1 to 0 [ 19 to   0]
red is 1 to -length    [ -1 to -20]

Game start loadout:
    wool 32
    bow
    arrows 2

Every build time
    wool 16

Every death
    wool 4
    bow
    arrows 2

Every 2 seconds
    restock their arrows back to 2
'''


from pathlib import Path
import os,subprocess
from mcpi import minecraft
from sportsRef import *
import time
#import signal
from math import floor
import traceback

#########################
#  Starting the Server  #
#########################

#quell the script's anger
if Path(".gitignore").exists():
    print("continue")
else:
    print("The script will get angry if run in the wrong directory.")
    print("Please try again after running this:")
    print("cd " + str(Path(__file__).parent))
    exit()

env = os.environ.copy()
ogwd = str(Path(__file__).parent)

name = "turfwars"

#Start a server
subprocess.run([
    "rm",
    "-r",
    name+"_files/games"])
Path(name+"_files/games/com.mojang/minecraftWorlds/").mkdir(parents=True, exist_ok=True)
subprocess.run([
    "cp", 
    "-r", 
    name+"_files/"+name, 
    name+"_files/games/com.mojang/minecraftWorlds/"])
#input()

env["MCPI_API_PORT"] = "4706"
pT = subprocess.Popen(
[ogwd+"/minecraft-pi-reborn-3.0.0-amd64.AppImage","--server"],
cwd=Path(name+"_files"),
env=env,
start_new_session=False #hopefully puts it in another group
)
print("PID:",pT.pid)

time.sleep(5) #giving the server enough time to start...





###########################
#  Connecting to the API  #
###########################

mcT = minecraft.Minecraft.create("localhost",4706)

#mcT.reborn.enableCompatMode() #only thing I know this does is force me to use ascii()
#it also changes the way mcB.getEntities(-1) works
mcT.postToChat("Api test from turfwars.py")
mcT.setting("world_immutable",1)


######################
#  Building the map  #
######################

mW = mapWidth = 10 / 2
mL = mapLength = 20 / 2 
mY = mapYLevel = -40
mH = mapHeight = 20 #this is also the height players are dropped from for the original dock in health
mO = mapOffset = 0 #variable used to keep score. Yes, I know it's stupid. 

redSpawn = (0,mapYLevel+1,-mapLength - 3)
blueSpawn = (0,mapYLevel+1,mapLength + 2)

def buildMap(t = "everything"):
    #options: 
    #  Everything
    #  "just floors" only the red and blue floors



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


################################
#  Choosing player teams loop  #
################################
try:
    mcT.reborn.disableCompatMode()
    def lowestPlayerHeight(): #only exists cause I can't do this in one line with lambda or whatver so it dont' error
        if playerHeights != []:
            return min(playerHeights)
        else: return 0
    def getPlayerTeams(players):
        output = {}
        for i in players:
            pos = mcT.entity.getPos(i)
            if pos.y > 55: #make sure they on a platform
                if (pos.z >0 )and (-3 < pos.x <3):
                    print(ascii(mcT.entity.getName(i))," is on team blue")
                    output[i] = 0
                if (pos.z <0) and (-3 < pos.x <3):
                    print(ascii(mcT.entity.getName(i))," is on team red")
                    output[i] = 1
                if (pos.x >0 )and (-3 < pos.z <3):
                    print(ascii(mcT.entity.getName(i))," is on team green")
                    output[i] = 2
                if (pos.x <0) and (-3 < pos.z <3):
                    print(ascii(mcT.entity.getName(i))," is on team banana")
                    output[i] = 3
        return output
    #Matchmaking loop
    players,oldPlayers = [],[]
    playerHeights = []
    playerTeams = {}

    countdownTillGameStart = 5
    timer = 0
    while False: 
        oldPlayers=players
        
        try: players = mcT.getPlayerEntityIds() #weird error 
        except Exception:
            traceback.print_exc()
            time.sleep(0.5)
            players = mcT.getPlayerEntityIds()
        #Traceback (most recent call last):
#   File "/home/beiop/Documents/vs/mcpi-servers/turfwars.py", line 204, in <module>
#     players = mcT.getPlayerEntityIds()
#               ^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/beiop/Documents/vs/mcpi-servers/mcpi/minecraft.py", line 370, in getPlayerEntityIds
#     return list(map(int, ids.split("|")))
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ValueError: invalid literal for int() with base 10: '3.0.0'

        
        #Welcome the latest player
        if len(oldPlayers) < len(players):
            print(players[:-1])
            mcT.postToChat("Wlecome " + ascii(mcT.entity.getName(players[-1])))
        
        #Get player heights
        playerHeights = []
        for player in players:
            pos = mcT.entity.getPos(player)
            if pos.y < 50:
                mcT.entity.setPos(player,0.5,pos.y+100,0.5)
            playerHeights.append(pos.y)
            
        #detect whether or not to start the countdown & run the countdown
        if len(players) > 1 and (lowestPlayerHeight() >= 56.5):
            if timer>2:
                mcT.postToChat("Game starting in " + str(countdownTillGameStart))
                countdownTillGameStart -= 1
                timer = 0
            if countdownTillGameStart < 1:
                playerTeams = getPlayerTeams(players)
                break
        else:
            if countdownTillGameStart <5:
                mcT.postToChat("Countdown Aborted :(")
            countdownTillGameStart = 5
        
        if timer <3:
            timer += 1
        
        time.sleep(.1)
    print(players)
    players = mcT.getPlayerEntityIds()
    if playerTeams == {}:
        while len(players) < 2:
            time.sleep(2)
            print("waiting")
            players = mcT.getPlayerEntityIds()
        for i in range(len(players)):
            playerTeams[players[i]] = i
    mcT.setting("world_immutable",0)
except Exception:
    traceback.print_exc()
    print("ignore next line, actually failed in team picking loop")
    pT.kill()
    #os.killpg(pT.pid, signal.SIGKILL)import traceback




###############
#  Game Loop  #
###############
mcT.reborn.enableCompatMode()
try:
    playerNamesToIds = dict()
    for player in players:
        playerNamesToIds[mcT.entity.getName(player)]=player
except Exception:
    traceback.print_exc()
    print("failed durring the playerNamesToIds definition")

global clock_start, wait_time_old, wait_time
clock_start = time.clock_gettime(6)
wait_time_old = 0.0

def wait(t): #sleep until t seconds elapsed since last issue of wait.
    global wait_time_old
    waited = 0
    wait_time = wait_time_old + t
    #print((clock_start + wait_time) - time.clock_gettime(6))
    while (time.clock_gettime(6)<clock_start + wait_time):
        waited += 1
        time.sleep(0.01)
    print(waited)
    wait_time_old = wait_time

def startWaiting(t):
    global waitUntilNow
    waitUntilNow = time.clock_gettime(6) + t
def waitingNotDone():
    now = time.clock_gettime(6)
    print(waitUntilNow - now)
    if now >= waitUntilNow:
        return False
    else:
        return True


def find_nearby_id(entities, hitx, hity, hitz):
    for entry in entities: 
        eid, etype, x, y, z = entry
        if (1.1 + hitx > x > hitx +-0.1) and (1.1 + hity > y > hity +-0.1) and (1.1 + hitz > z > hitz +-0.1):
            return eid
    print("didn't find nothing")
    return None

try:
    for player in players: #teleport players and give them their starting loadouts.
        if playerTeams[player] == 0: #if on blue team
            pos = blueSpawn
            mcT.entity.spawnItem(*pos,*blueWool(32))
            
        if playerTeams[player] == 1: # if on red team
            pos = redSpawn
            mcT.entity.spawnItem(*pos,*redWool(32))
        mcT.entity.spawnItem(*pos,arrow,2)
        mcT.entity.spawnItem(*pos,bow)
        mcT.entity.setPos(player,pos[0],pos[1]+mH-1,pos[2])

    while True:
        startWaiting(30) #run loop before for 30 seconds about
        mcT.postToChat("30 seconds of building!")
        
        while waitingNotDone():
            
            try:
                for player in players:
                    mcT.world.removeEntities(80)
                    pos = mcT.entity.getPos(player)
                    team = playerTeams[player]
                    if team == 0:
                        if pos.z < 0:
                            mcT.entity.setVelocity(player,0,1,1000)
                            #mcT.postToChat("bro on the wrong side.")
                    if team == 1:
                        if pos.z > 0:
                            mcT.entity.setVelocity(player,0,1,-1000)
                            #mcT.postToChat("bro on the wrong side.")
                    
                    if pos.y > -10:
                        if team == 0:
                            mcT.entity.setPos(player,blueSpawn)
                        if team == 1:
                            mcT.entity.setPos(player,redSpawn)
            except Exception:
                traceback.print_exc()
                players = mcT.getPlayerEntityIds()
            #time.sleep(1)

        justGotDoneBuilding = True

        mcT.postToChat("1 minute of fighting!")
        mcT.setBlocks(mapWidth,mapYLevel+1,mO,-mapWidth,mapYLevel+20,mO,air)
        playersWhoShotArrows = []
        for i in range(30):
            for i in playersWhoShotArrows:
                for player in players:
                    if justGotDoneBuilding == True: #give everyone one arrow 
                        pos = mcT.entity.getPos(player)
                        mcT.entity.spawnItem(pos,arrow,1)
                        justGotDoneBuilding = False
                    if player in playersWhoShotArrows:
                        pos = mcT.entity.getPos(player)
                        mcT.entity.spawnItem(pos,arrow,playersWhoShotArrows[player])
            startWaiting(2)
            playersWhoShotArrows = []
            while waitingNotDone():
                try:
                    for player in players:
                        pos = mcT.entity.getPos(player)
                        team = playerTeams[player]
                        if team == 0:
                            if pos.z < 0:
                                mcT.entity.setVelocity(player,0,1,1000)
                                #mcT.postToChat("bro on the wrong side.")
                        if team == 1:
                            if pos.z > 0:
                                mcT.entity.setVelocity(player,0,1,-1000)
                                #mcT.postToChat("bro on the wrong side.")
                        if pos.y > -10:
                            if team == 0:
                                mcT.entity.setPos(player,blueSpawn)
                            if team == 1:
                                mcT.entity.setPos(player,redSpawn)
                except Exception:
                    traceback.print_exc()
                    players = mcT.getPlayerEntityIds()

                

                hits = mcT.events.pollProjectileHits()
                print(hits)
                mcT.reborn.disableCompatMode()

                projectiles = mcT.getEntities(80)
                print(projectiles)
                mcT.reborn.enableCompatMode()
                
                for hit in hits:
                    
                    print(hit.pos, hit.face, hit.originName, hit.targetName)
                    
                    if hit.targetName != "":
                        print(hit.targetName,"was hit")
                        try:
                            var1 = playerTeams[mcT.getPlayerEntityId(hit.targetName)]
                            print(var1,mcT.getPlayerEntityId(hit.targetName))
                            if var1 == 1:
                                mO -= 1
                                mcT.postToChat("blue scores!" + str(mO))
                            if var1 == 0:
                                mO += 1
                                mcT.postToChat("red scores!"+str(mO))
                            if playerNamesToIds[hit.orginName] in playersWhoShotArrows:
                                if playersWhoShotArrows[playerNamesToIds[hit.orginName]] < 2:
                                    playersWhoShotArrows[playerNamesToIds[hit.orginName]] += 1
                            else:
                                playersWhoShotArrows[playerNamesToIds[hit.orginName]] = 1

                            
                        except Exception:
                            traceback.print_exc()
                    else: #if targetName is nothing, try 
                        this = find_nearby_id(projectiles,hit.pos.x,hit.pos.y,hit.pos.z)

                        if this != None:
                            mcT.removeEntity(this)
                            if (mapWidth>= hit.pos.x >= -mapWidth) and (mapLength >= hit.pos.z >= -mapLength): #check if it is within the map
                                print("removing block at",pos)
                                mcT.setBlock(hit.pos,air)
                                if hit.pos.z > 0:
                                    mcT.entity.spawnItem(hit.pos.x,hit.pos.y,hit.pos.z,redWool)
                                if hit.pos.z < 0:
                                    mcT.entity.spawnItem(hit.pos.x,hit.pos.y,hit.pos.z,blueWool)
                #time.sleep(1)
        print("exite")
        
except Exception:
    traceback.print_exc()
    pT.kill()
    #os.killpg(pT.pid, signal.SIGKILL)
print("kablouey")