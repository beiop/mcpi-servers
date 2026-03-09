from pathlib import Path
#import os,subprocess
from mcpi import minecraft
from sportsRef import *
import time
from math import floor


mcB = minecraft.Minecraft.create("localhost",4707)

mcB.postToChat("Api test from stores.py")
mcB.reborn.disableCompatMode() #only thing I know this does is force me to use ascii()
#it also changes the way mcB.getEntities(-1) works

print(mcB.getEntities)
 