#! /usr/bin/env python3
import time
import argparse
import os
import os.path
from os import path
import random
from datetime import datetime
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import json
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
args = parser.parse_args()
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

stepperkit = MotorKit(address=0x61)
dcmotorkit = MotorKit()
settings = {
    dcmotor1 = 0
    dcmotor2 = 0
    stepperSpeed = 0
}
sDaemon = None

def stepperDaemon():
    global settings
    ss = abs(settings["stepperSpeed"])
    while True:
        if settings["stepperSpeed"] != 0:
            if settings["stepperSpeed"] > 0:
                stepperkit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            else:
                stepperkit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(1/ss)
        else:
            time.sleep(0.01)

def setMotorSpeed(motor, speed):
    global direction
    if motor == 1:
        dcmotorkit.motor1.throttle = speed
    if motor == 2:
        dcmotorkit.motor2.throttle = speed
    if motor == 3:
        dcmotorkit.motor3.throttle = speed
    if motor == 4:
        dcmotorkit.motor4.throttle = speed

@app.route("/")
def default_route():
    global settings
    motor = request.args["m"]
    speed = float(request.args["s"])
    if "dcmotor" in motor:
        dcm = int(motor.replace("dcmotor",""))
        setMotorSpeed(dcm, speed)
    settings[motor] = speed

if __name__ == "__main__":
    sDaemon = threading.Thread(target=stepperDaemon, daemon=True)
    sDaemon.start()
    app.run(host=args.ip, port=80, debug=True)