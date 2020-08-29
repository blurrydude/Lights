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
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
args = parser.parse_args()
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

stepperkit = MotorKit(address=0x61)
dcmotorkit = MotorKit()
settings = {
    "dcmotor1": 0,
    "dcmotor2": 0,
    "stepper": 0
}
sDaemon = None
cDaemon = None

def stepperDaemon():
    global settings
    ss = abs(settings["stepper"])
    while True:
        if settings["stepper"] != 0 and ss != 0:
            if settings["stepper"] > 0:
                stepperkit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            else:
                stepperkit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(1/ss)
        else:
            time.sleep(0.01)

def checkCommandDaemon():
    global settings
    while True:
        command_topic = requests.get('https://blurrydude.com:5000/topic?t=commands').text.lower()
        if len(command_topic) > 2:
            print('command topic: '+command_topic)
            if "motor" in command_topic:
                requests.get('https://blurrydude.com:5000/ack?t=commands')
                if "dc" in command_topic:
                    if "run" in command_topic:
                        if "1" in command_topic or "one" in command_topic:
                            print('DC Motor 1 Run')
                            settings["dcmotor1"] = 1
                            setMotorSpeed(1,1)
                        elif "2" in command_topic or "two" in command_topic:
                            print('DC Motor 2 Run')
                            settings["dcmotor2"] = 1
                            setMotorSpeed(2,1)
                    elif "stop" in command_topic:
                        if "1" in command_topic or "one" in command_topic:
                            print('DC Motor 1 Stop')
                            settings["dcmotor1"] = 1
                            setMotorSpeed(1,0)
                        elif "2" in command_topic or "two" in command_topic:
                            print('DC Motor 2 Stop')
                            settings["dcmotor2"] = 1
                            setMotorSpeed(2,0)
                elif "stepper" in command_topic:
                    if "run" in command_topic:
                        if "forward" in command_topic:
                            print('Stepper Motor Forward')
                            settings["stepper"] = 200
                        elif "backward" in command_topic:
                            print('Stepper Motor Backward')
                            settings["stepper"] = -200
                    elif "stop" in command_topic:
                        print('Stepper Motor Stop')
                        settings["stepper"] = 0
    time.sleep(2)
                

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
    cDaemon = threading.Thread(target=checkCommandDaemon, daemon=True)
    cDaemon.start()
    app.run(host=args.ip, port=80, debug=True)