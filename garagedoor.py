import pifacedigitalio as p
import time
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
args = parser.parse_args()
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

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

@app.route("/", methods=["GET"])
def set_endpoint():
    command = request.args["c"]
    if command == "open":
        openDoor()
    if closeDoor == "close":
        openDoor()
    if command == "half":
        setDoorHalf()

if __name__ == "__main__":
    p.init()
    app.run(host=args.ip, port=80, debug=True)