
from pathlib import Path
import os,subprocess
from mcpi import minecraft

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


#Start a server
subprocess.run([
    "rm",
    "-r",
    "sports_files/games"])
Path("sports_files/games/com.mojang/minecraftWorlds/").mkdir(parents=True, exist_ok=True)
subprocess.run([
    "cp", 
    "-r", 
    "sports_files/sports", 
    "sports_files/games/com.mojang/minecraftWorlds/"])
input()

env["MCPI_API_PORT"] = "4707"
pB = subprocess.Popen(
[ogwd+"/minecraft-pi-reborn-3.0.0-amd64.AppImage","--server"],
cwd=Path("sports_files"),
env=env
)
input()


input()
pB.terminate()