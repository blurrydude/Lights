import pifacedigitalio as p
import time
p.init()

def waitFor(i):
    while p.digital_read(i) == 0: # FLIP THIS WHEN REED SWITCH IS INSTALLED
        time.sleep(0.1)

def openDoor():
    p.digital_write(0,1)
    time.sleep(0.2)
    p.digital_write(0,0)

def closeDoor(closeto=0):
    p.digital_write(0,1)
    waitFor(closeto)
    time.sleep(0.5)
    p.digital_write(0,0)

def setDoorHalf():
    if p.digital_read(0) == 1:
        openDoor()
        waitFor(1)
    elif p.digital_read(1) == 0:
        closeDoor(1)
        time.sleep(0.1)
        openDoor()

setDoorHalf()