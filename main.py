#quell the script's anger
from pathlib import Path

if Path(".gitignore").exists():
    print("continue")
else:
    print("The script will get angry if run in the wrong directory.")
    print("Please try again after running this:")
    print("cd " + str(Path(__file__).parent))
    exit()

import subprocess, time
from mcpi import minecraft

subprocess.run(["mkdir", "-p","backup"])
CWD=Path(__file__).parent


while True:
    
    print("[Python] Starting Server")
    p = subprocess.Popen("./minecraft-pi-reborn-server-2.5.4-amd64.AppImage",cwd=CWD
)

    time.sleep(60)
    print("[PYTHON] connecting to API")
    mc = minecraft.Minecraft.create()
    mc.postToChat("API connected!")
    
    #wait awhile before updating again
    time.sleep(86400) #604800
    mc.postToChat("5 minutes till server restarts for backup")
    time.sleep(60)
    mc.postToChat("4 minutes till server restarts for backup")
    time.sleep(60)
    mc.postToChat("3 minutes till server restarts for backup")
    time.sleep(60)
    mc.postToChat("2 minutes till server restarts for backup")
    time.sleep(60)
    mc.postToChat("1 minute till server restarts for backup")
    time.sleep(60)

    mc.postToChat("Server restarting")
    p.terminate()

    print("[Python] Giving server 5 seconds to stop")
    time.sleep(5)

    print("[Python] Backing up world files")
    subprocess.run(["mkdir", "-p","backup"])
    subprocess.run(["cp", "-r", "games/com.mojang/minecraftWorlds/pbpt", "backup"])
    subprocess.run("zip -r backup/pbpt_$(date +'%Y-%m-%d').zip backup/pbpt", shell=True)
    subprocess.run(["rm", "-r","backup/pbpt"])
