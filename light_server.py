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
import socket

name = socket.gethostname()
parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--ledcount", "-n", help="led count")
args = parser.parse_args()
led_count = int(args.ledcount)
app = FlaskAPI(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
pixels = neopixel.NeoPixel(board.D18, led_count)
mem = []
config = {}

def load_config():
    global config
    hasConfig = path.exists('/home/pi/light_conf.json')
    if hasConfig == False:
        config = {
            "autosun": True,
            "personality": True,
            "lastattention": time.time(),
            "lat": 39.8888672,
            "lon": -84.217542
        }
        save_config()

    with open('/home/pi/light_conf.json', "r") as read_file:
        config = json.load(read_file)

def save_config():
    with open('/home/pi/light_conf.json', "w") as write_file:
        json.dump(config, write_file, indent=4)

def save_memory(memory):
    with open('/home/pi/light_mem.json', "w") as write_file:
        json.dump(memory, write_file, indent=4)

def load_memory():
    global mem
    hasMem = path.exists('/home/pi/light_mem.json')
    if hasMem == False:
        for i in range(led_count):
            mem.append((0,0,0))
        save_memory()
    try:
        with open('/home/pi/light_mem.json', "r") as read_file:
            mem = json.load(read_file)
        return mem
    except:
        for i in range(led_count):
            mem.append((0,0,0))
        os.remove('/home/pi/light_mem.json')
        with open('/home/pi/light_mem.json', "w") as write_file:
            json.dump(mem, write_file, indent=4)

@app.route("/", methods=['GET'])
def light_endpoint():
    global mem
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
    global mem
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

@app.route("/template", methods=['GET'])
def template_endpoint():
    page = request.args['p']
    pageFile = open("/home/pi/Lights/"+page,"r")
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
    a = int(request.args['a'])
    p = mem[a]

    return str(p[0])+','+str(p[1])+','+str(p[2])

@app.route("/mem", methods=['GET'])
def mem_endpoint():
    config['lastattention'] = time.time()
    save_config()
    return mem

@app.route("/config", methods=['GET'])
def config_endpoint():
    config['name'] = name
    return config

@app.route("/setautosun", methods=['GET'])
def setautosun_endpoint():
    config['autosun'] = bool(request.args['v'])
    save_config()
    return config

@app.route("/setpersonality", methods=['GET'])
def setpersonality_endpoint():
    config['personality'] = bool(request.args['v'])
    save_config()
    return config


@app.route("/checkneighbors", methods=['GET'])
def checkneighbors_endpoint():
    directory = r'/home/pi/'
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".neighbor"):
            f = open(filename, 'r')
            t = f.read()
            f.close()
            results.append(t)
    return results

if __name__ == "__main__":
    load_memory()
    load_config()
    app.run(host=args.ip, port=80, debug=True)
    # app.run(ssl_context=('/etc/letsencrypt/live/blurrydude.com/fullchain.pem','/etc/letsencrypt/live/blurrydude.com/privkey.pem'), host='192.168.1.51')
