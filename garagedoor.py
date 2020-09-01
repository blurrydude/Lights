import pifacedigitalio as p
import time
p.init()

def waitFor(i):
    while p.digital_read(i) == 0: # FLIP THIS WHEN REED SWITCH IS INSTALLED
        time.sleep(0.1)

def openDoor():
    p.digital_write(0,1)
    time.sleep(0.5)
    p.digital_write(0,0)

def closeDoor():
    p.digital_write(0,1)
    waitFor(1)
    p.digital_write(0,0)

openDoor()
time.sleep(2)
closeDoor()