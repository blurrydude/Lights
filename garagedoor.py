import pifacedigitalio as p
import time
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--s", "-s", help="whether or not to use sensor input (0 or 1)")
args = parser.parse_args()
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

sensors = args.s == "1"
dooropen = False

def waitFor(i):
    ticks = 0
    while p.digital_read(i) == 0 and ticks < 1500:
        time.sleep(0.01)
        ticks = ticks + 1

def openDoor():
    global dooropen
    if dooropen == True:
        return
    p.digital_write(0,1)
    time.sleep(0.2)
    p.digital_write(0,0)
    time.sleep(10)
    dooropen = True

def closeDoor():
    global dooropen
    p.digital_write(0,1)
    time.sleep(20)
    p.digital_write(0,0)
    time.sleep(0.2)
    dooropen = False

def closeDoorWithSensors(closeto=0):
    p.digital_write(0,1)
    if sensors == True:
        waitFor(closeto)
    else:
        time.sleep(10)
    time.sleep(0.5)
    p.digital_write(0,0)
    dooropen = False

def setDoorHalf():
    if p.digital_read(1) == 1:
        return
    if p.digital_read(0) == 1:
        openDoor()
        waitFor(1)
        openDoor()
    elif p.digital_read(2) == 1:
        closeDoor()
        waitFor(1)
        openDoor()

@app.route("/", methods=["GET"])
def set_endpoint():
    command = request.args["c"]
    if "close" in command:
        if sensors == True:
            closeDoorWithSensors()
        else:
            closeDoor()
    elif ("half" in command or "crack" in command) and sensors == True:
        setDoorHalf()
    elif "open" in command:
        openDoor()
    return "OK"

@app.route("/alive", methods=["GET"])
def alive_endpoint():
    return "I'm alive"

@app.route("/status", methods=["GET"])
def status_endpoint():
    if sensors == True:
        if p.digital_read(0) == 1:
            return "closed"
        elif p.digital_read(1) == 1:
            return "half"
        elif p.digital_read(2) == 1:
            return "open"
        else:
            return "unknown"
    else:
        if dooropen == True:
            return "open"
        else:
            return "closed"

if __name__ == "__main__":
    #print('wait a minute')
    dooropen = False
    time.sleep(10)
    p.init()
    app.run(host=args.ip, port=80)