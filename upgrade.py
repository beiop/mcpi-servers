#script to move the world files to the correct dirs so they work with the new script.

from pathlib import Path
import subprocess


Path("anarchy_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("survival_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"
Path("creative_files").mkdir(parents=True, exist_ok=True)  # thing that creates folder, similar to mkdir", "-p"

subprocess.run(["mv","sdk","anarchy_files/sdk"])
subprocess.run(["mv","backup","anarchy_files/backup"])
subprocess.run(["mv","games","anarchy_files/games"])
subprocess.run(["mv","mods","anarchy_files/mods"])
subprocess.run(["mv","blacklist.txt","anarchy_files/blacklist.txt"])
#subprocess.run(["mv","server.properties","anarchy_files/server.properties"])
