#quell the script's anger
from pathlib import Path

if Path(".gitignore").exists():
    print("continue")
else:
    print("The script will get angry if run in the wrong directory.")
    print("Please try again after running this:")
    print("cd " + str(Path(__file__).parent))
    exit()

import subprocess, os
import time
from mcpi import minecraft
import datetime
now = datetime.datetime.now()
def rn(strin):return '\033[92m' + strin + " " + str(now.time()) + ' \033[96m'


#Making various directories to avoid errors later
Path("anarchy_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("survival_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("creative_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("anarchy_files/backup").mkdir(parents=True, exist_ok=True)
Path("survival_files/backup").mkdir(parents=True, exist_ok=True)
Path("creative_files/backup").mkdir(parents=True, exist_ok=True)


env = os.environ.copy()

ogwd = str(Path(__file__).parent)


while True:
    
    print(rn("[Python] Starting Servers"))
    
    env["MCPI_API_PORT"] = "4709"
    pa = subprocess.Popen(
    [ogwd+"/minecraft-pi-reborn-server-2.5.4-amd64.AppImage"],
    cwd=Path("anarchy_files"),
    env=env
    )
    env["MCPI_API_PORT"] = "4708"
    ps = subprocess.Popen(
    [ogwd+"/minecraft-pi-reborn-server-2.5.4-amd64.AppImage"],
    cwd=Path("survival_files"),
    env=env
    )
    env["MCPI_API_PORT"] = "4710"
    pc = subprocess.Popen(
    [ogwd+"/minecraft-pi-reborn-server-2.5.4-amd64.AppImage"],
    cwd=Path("creative_files"),
    env=env
    )
    
    time.sleep(120) #60 seconds was enough for one server, now it's arbitrary amount for three servers. This is only nessisary the first time the world is generated
    print(rn("[PYTHON] testing APIs"))
    mcA = minecraft.Minecraft.create("localhost",4709)
    mcS = minecraft.Minecraft.create("localhost",4708)
    mcC = minecraft.Minecraft.create("localhost",4710)


    #ai that's supposed to run the same thing on them all
    class MultiMC:
        def __init__(self, *servers):
            self.servers = servers

        def __getattr__(self, name):
            def method(*args, **kwargs):
                for m in self.servers:
                    getattr(m, name)(*args, **kwargs)
            return method

    mc = MultiMC(mcA, mcS, mcC)
    mc.postToChat("API working!")
    
    #wait awhile before updating again
    time.sleep(4) #86400 seconds in one day 43200
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
    
    
    ps.terminate()
    pa.terminate()
    pc.terminate()

    print(rn("[Python] Giving server 5 seconds to stop"))
    time.sleep(5)

    #anarchy
    subprocess.run([
        "cp",
        "-r",
        "anarchy_files/games/com.mojang/minecraftWorlds/pbpt",
        "anarchy_files/backup"])
    subprocess.run([
        "zip", 
        "-r",
        "-j",
        f"anarchy_files/backup/anarchy_{datetime.datetime.now().strftime('%m-%d-%Y_%H-%M')}.zip",
        "anarchy_files/backup/pbpt/"])
    subprocess.run([
        "rm",
        "-r",
        "anarchy_files/backup/pbpt"])
    #survival
    subprocess.run([
        "cp",
        "-r",
        "survival_files/games/com.mojang/minecraftWorlds/survival",
        "survival_files/backup"])
    subprocess.run([
        "zip", 
        "-r",
        "-j",
        f"survival_files/backup/survival_{datetime.datetime.now().strftime('%m-%d-%Y_%H-%M')}.zip",
        "survival_files/backup/survival/"])
    subprocess.run([
        "rm",
        "-r",
        "survival_files/backup/survival"])
    #creative
    subprocess.run([
        "cp",
        "-r",
        "creative_files/games/com.mojang/minecraftWorlds/creative",
        "creative_files/backup"])
    subprocess.run([
        "zip", 
        "-r",
        "-j",
        f"creative_files/backup/creative_{datetime.datetime.now().strftime('%m-%d-%Y_%H-%M')}.zip",
        "creative_files/backup/creative/"])
    subprocess.run([
        "rm",
        "-r",
        "creative_files/backup/creative"])
