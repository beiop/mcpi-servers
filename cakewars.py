
from pathlib import Path
import os,subprocess
from mcpi import minecraft
import time

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

name = "cakewars"

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
input()

env["MCPI_API_PORT"] = "4707"
pB = subprocess.Popen(
[ogwd+"/minecraft-pi-reborn-3.0.0-amd64.AppImage","--server"],
cwd=Path(name+"_files"),

env=env
)
input()


input()
pB.terminate()
time.sleep(1)