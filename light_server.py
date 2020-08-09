#! /usr/bin/env python3
from evdev import InputDevice, categorize, ecodes
import board
import neopixel
import time
import argparse
import os
import os.path
from os import path
import random
import datetime
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--ledcount", "-n", help="led count")
args = parser.parse_args()
led_count = int(args.ledcount)
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
pixels = neopixel.NeoPixel(board.D18, led_count)
mem = []

for i in range(led_count):
    mem.append((0,0,0))

@app.route("/", methods=['GET'])
def light_endpoint():
    a = int(request.args['a'])
    r = int(request.args['r'])
    g = int(request.args['g'])
    b = int(request.args['b'])
    z = int(request.args['z'])
    while a <= z:
        pixels[a] = (r, g, b)
        mem[a] = (r, g, b)
        a = a + 1
    return "OK"

@app.route("/query/<int:a>", methods=['GET'])
def light_query_endpoint():
    a = int(request.args['a'])
    p = mem[a]

    return str(p[0])+','+str(p[1])+','+str(p[2])

if __name__ == "__main__":
    app.run(host=args.ip)
    # app.run(ssl_context=('/etc/letsencrypt/live/blurrydude.com/fullchain.pem','/etc/letsencrypt/live/blurrydude.com/privkey.pem'), host='192.168.1.51')
