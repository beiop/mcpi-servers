# mcpi-servers
server backup script &amp; mayube sports

# terrible layout rn
```
sports.py - Starts the server
 \---py.py - 1 loop to choose teams and then one game loop
        \---py3.py - the actuall game loop
                \---apiworker.py - script for speedy api
```
# end goal
```
sports.py - Starts the server
    \---apiworker.py - script for speedy api
```
```
Team choosing loop
    checks all player locations
Game loop
    o spawns items ~20 calls
    sale script loop
        i checks if they are in stores ~ 80 calls
        o makes sales at stores ~0-8 calls
    i checks for cake deaths 4 calls
    i checks for player deaths 4+ calls
    o teleport them around 4+
```



## todo ig
1 website that checks every hour

2 server that runs 
    script that backs that up every week twice 
        OPTIONAL (only 5 seconds after the world saves)
        (store it on the nas or something)

----
#### Port list:
| server port | api port | internal server name    | Api alias  | World files |
|-------------|----------|-------------------------|------------|-------------|
| 19136       | 4710     | Beiop Creative          | mcC        | creative... |
| 19135       | 4709     | Pbpt Anarchy 2          | mcA        | anarchy...  |
| 19134       | 4708     | Beiop Survival          | mcS        | survival... |
| 19137       | 4707     | Beiop Cake Wars         | mcB & mcB2 | cakewars... | aka "sports..."
| 19138       | 4706     | Beiop Turf Wars         | mcT        | turfwars... |


----
Shorter term todo list:

* DONE - Need to be able to change ports on api
* DONE - Need to be able to run 2 instances on same port.
* DONE - find a way to run minecraft from a different directory
* DONE - Make script to move the old world files from their old locations to the new ones
* THEY DONT??!?! - Check if ports 19132-19135 show up when port forwarding
* DONE - Make the new script use the new dirs for the main server
* DONE - run N number of servers separate from each other
* CHOCOLATE BREAK!!!
* DONE - Teleport players as soon as they join
* DONE - sort players into teams by making them climb ladders
* NOPE - Only start game when players are on different platforms.
* CHOCOLATE BREAK!!!
* NEXT - make stacks of 64 of items
* NEXT - test running a store

* NEXT - Replace beds with cake
* NEXT - Detect death and respawn players by their cake
* NEXT - attempt to optimise the code


----



Another todo list:


_ _



_ _

_ _
#### I just needed somewhere to put this:

```
RUN_DIR = Path("/path") 

```
3.0.0 version:
Try Downloading The Game From Multiple Sources (And Add A Timeout)

things I want players to be able to get

obsidian
wool
wood
snow
tnt
lava* Lag?? Could be solved by lowering the play area closer to the void
same thing with water
bows
arrows
food

Things I dont want them to be able to get

beds