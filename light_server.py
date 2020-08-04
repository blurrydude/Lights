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

led_count = 16
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
pixels = neopixel.NeoPixel(board.D18, led_count)

@app.route("/", methods=['GET'])
def light_endpoint():
    print(request.data)
    r = int(request.args['r'])
    g = int(request.args['g'])
    b = int(request.args['b'])
    a = int(request.args['a'])
    z = int(request.args['z'])
    while a <= z:
        pixels[a] = (r, g, b)
        a = a + 1
    return "OK"

if __name__ == "__main__":
    app.run(host='192.168.1.53')
    # app.run(ssl_context=('/etc/letsencrypt/live/blurrydude.com/fullchain.pem','/etc/letsencrypt/live/blurrydude.com/privkey.pem'), host='192.168.1.51')
