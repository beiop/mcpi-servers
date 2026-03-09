#a script to run one 3.0.0 server and back it up hourly


#quell the script's anger
from pathlib import Path

if Path(".gitignore").exists():
    print("continue")
else:
    print("The script will get angry if run in the wrong directory.")
    print("Please try again after running this:")
    print("cd " + str(Path(__file__).parent))
    exit()
import signal
import subprocess, os
import time
from mcpi import minecraft
import datetime

def rn(strin):return '\033[92m' + strin + " " + str(datetime.datetime.now().strftime('%m-%d-%Y_%H-%M-%S')) + ' \033[96m'


#Making various directories to avoid errors later
Path("test_world_for_sports_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("test_world_for_sports_files/backup").mkdir(parents=True, exist_ok=True)


env = os.environ.copy()

ogwd = str(Path(__file__).parent)


while True:
    
    #Script backs up servers first for now

    #anarchy
    subprocess.run([
        "cp",
        "-r",
        "test_world_for_sports_files/games/com.mojang/minecraftWorlds/sports_building",
        "test_world_for_sports_files/backup"])
    subprocess.run([
        "zip", 
        "-r",
        "-j",
        f"test_world_for_sports_files/backup/sports_building_{datetime.datetime.now().strftime('%m-%d-%Y_%H-%M')}.zip",
        "test_world_for_sports_files/backup/sports_building/"])
    subprocess.run([
        "rm",
        "-r",
        "test_world_for_sports_files/backup/sports_building"])
   
    print(rn("[Python] Starting Servers"))
    
    #env["MCPI_API_PORT"] = "4711" #only used if setting to something other than the default
    pa = subprocess.Popen(
        [ogwd+"/minecraft-pi-reborn-3.0.0-amd64.AppImage","--server"],
        cwd=Path("test_world_for_sports_files"),
        preexec_fn=os.setsid #theoretically runs this and all it's children in a new process group so 
        )
    time.sleep(15) #60 seconds was enough for one server, now it's arbitrary amount for three servers. This is only nessisary the first time the world is generated
    
    if True: #this just for testing purposes.
        print(rn("[PYTHON] testing APIs"))
        
        
        mcA = minecraft.Minecraft.create("localhost",4711)
        

        #ai that's supposed to run the same thing on them all
        class MultiMC:
            def __init__(self, *servers):
                self.servers = servers

            def __getattr__(self, name):
                def method(*args, **kwargs):
                    for m in self.servers:
                        getattr(m, name)(*args, **kwargs)
                return method

        mc = MultiMC(mcA) #add other api aliases here eg: (mcA,mcB,mcC)
        mc.postToChat("API working!")
        
        #wait awhile before updating again
        time.sleep(3600) #86400 seconds in one day 43200 * 2 or 3600*24
        mc.postToChat("5 minutes till server restarts for backup.")
        time.sleep(3)
        mc.postToChat("Any changes made within the last 30 seconds before a restart")
        time.sleep(2)
        mc.postToChat("may not be saved.")
        time.sleep(55)
        mc.postToChat("4 minutes till server restarts for backup.")
        time.sleep(2)
        mc.postToChat("Any changes made within the last 30 seconds before a restart")
        time.sleep(1)
        mc.postToChat("may not be saved.")
        time.sleep(55)
        mc.postToChat("3 minutes till server restarts for backup.")
        time.sleep(2)
        mc.postToChat("Any changes made within the last 30 seconds before a restart")
        time.sleep(1)
        mc.postToChat("may not be saved.")
        time.sleep(55)
        mc.postToChat("2 minutes till server restarts for backup.")
        time.sleep(2)
        mc.postToChat("Any changes made within the last 30 seconds before a restart")
        time.sleep(1)
        mc.postToChat("may not be saved.")
        time.sleep(55)
        mc.postToChat("1 minute till server restarts for backup.")
        time.sleep(30)
        mc.postToChat("30 seconds till server restarts for backup.")
        time.sleep(30)
        mc.postToChat("Server restarting. Please disconnect and recconect.")
        time.sleep(1) #so the message of the server restarting goes through before the server disconnects.


    


    print(rn("[Python] attempting to kill now"))
    os.killpg(os.getpgid(pa.pid), signal.SIGTERM)

    print(rn("[Python] Giving server 5 seconds to stop"))
    time.sleep(5)
