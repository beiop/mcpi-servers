# mcpi-servers
server backup script &amp; downdetector for mcpi

## todo ig
1 website that checks every hour

2 server that runs 
    script that backs that up every week twice 
        OPTIONAL (only 5 seconds after the world saves)
        (store it on the nas or something)

----
#### Port list:

19136. Pbpt Anarchy 2 4711 <-- api ports
19135. Beiop Survival 4710
19134. Beiop Creative 4709
----
Shorter term todo list:

* DONE - Need to be able to change ports on api
* DONE - Need to be able to run 2 instances on same port.
* DONE - find a way to run minecraft from a different directory
* DONE - Make script to move the old world files from their old locations to the new ones
* NEXT - Check if ports 19132-19135 show up when port forwarding
* NEXT - Make the new script use the new dirs for the main server
* NEXT - run N number of servers separate from each other

----
_ _

_ _

_ _
#### I just needed somewhere to put this:

```
RUN_DIR = Path("/path") 

```
