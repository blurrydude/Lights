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
import json

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--ledcount", "-n", help="led count")
args = parser.parse_args()
led_count = int(args.ledcount)
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
pixels = neopixel.NeoPixel(board.D18, led_count)

def save_memory(mem):
    with open('/home/pi/light_mem.json', "w") as write_file:
        json.dump(mem, write_file, indent=4)

def load_memory():
    mem = []
    hasMem = path.exists('/home/pi/light_mem.json')
    if hasMem == False:
        for i in range(led_count):
            mem.append((0,0,0))
        with open('/home/pi/light_mem.json', "w") as write_file:
            json.dump(mem, write_file, indent=4)
    with open('/home/pi/light_mem.json', "r") as read_file:
        mem = json.load(read_file)
    return mem

@app.route("/", methods=['GET'])
def light_endpoint():
    mem = load_memory()
    a = int(request.args['a'])
    r = int(request.args['r'])
    g = int(request.args['g'])
    b = int(request.args['b'])
    z = int(request.args['z'])
    while a <= z:
        pixels[a] = (r, g, b)
        mem[a] = (r, g, b)
        a = a + 1
    save_memory(mem)
    return mem

@app.route("/pixels", methods=['GET'])
def pixels_endpoint():
    mem = load_memory()
    p = request.args['p'].split(",")
    r = int(request.args['r'])
    g = int(request.args['g'])
    b = int(request.args['b'])
    for i in p:
        pixels[int(p[i])] = (r, g, b)
        mem[int(p[i])] = (r, g, b)
    save_memory(mem)
    return mem

@app.route("/control", methods=['GET'])
def control_endpoint():
    pageFile = open("/home/pi/Lights/index.html","r")
    pageData = pageFile.read()
    pageFile.close()
    return pageData

@app.route("/version", methods=['GET'])
def version_endpoint():
    pageFile = open("/home/pi/lightdata.json","r")
    pageData = pageFile.read()
    pageFile.close()
    return pageData

@app.route("/query", methods=['GET'])
def light_query_endpoint():
    mem = load_memory()
    a = int(request.args['a'])
    p = mem[a]

    return str(p[0])+','+str(p[1])+','+str(p[2])

if __name__ == "__main__":
    load_memory()
    app.run(host=args.ip, port=80, debug=True)
    # app.run(ssl_context=('/etc/letsencrypt/live/blurrydude.com/fullchain.pem','/etc/letsencrypt/live/blurrydude.com/privkey.pem'), host='192.168.1.51')
