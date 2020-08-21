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
from datetime import datetime
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
neighbors = []
brain = {}

def load_config():
    global config
    hasConfig = path.exists('/home/pi/light_conf.json')
    if hasConfig == False:
        config = {
            "autosun": True,
            "personality": True,
            "lastattention": time.time(),
            "lat": 39.8888672,
            "lon": -84.217542,
            "ip": args.ip
        }
        save_config()

    with open('/home/pi/light_conf.json', "r") as read_file:
        config = json.load(read_file)
    if "ip" not in config.keys():
        config["ip"] = args.ip

def load_neighbors():
    global neighbors
    directory = r'/home/pi/'
    neighbors = []
    for filename in os.listdir(directory):
        try:
            if filename.endswith(".neighbor"):
                f = open("/home/pi/"+filename, 'r')
                t = f.read()
                f.close()
                neighbors.append(t)
        except:
            log("Unexpected error reading neighbors")
            try:
                os.remove("/home/pi/"+filename)
                continue
            except:
                log("Unexpected error removing neighbors")
                continue
def log(message):
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    message = date_time + ": " + message
    with open('/home/pi/light_server_log_'+datetime.now().strftime("%Y-%m-%d")+'.log', "a+") as write_file:
        write_file.write(message+"\n")

def save_config():
    config["ip"] = args.ip
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
        save_memory(mem)
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

def save_brain():
    with open('/home/pi/brain.json', "w") as write_file:
        json.dump(brain, write_file, indent=4)

def load_brain():
    global brain
    hasbrain = path.exists('/home/pi/brain.json')
    if hasbrain == False:
        save_brain()
    with open('/home/pi/brain.json', "r") as read_file:
        brain = json.load(read_file)

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
    return neighbors

@app.route("/weather", methods=['GET'])
def weather_endpoint():
    pageFile = open("/home/pi/weather.json","r")
    pageData = pageFile.read()
    pageFile.close()
    return pageData

@app.route("/converse", methods=['GET'])
def converse_endpoint():
    sep=", "
    thing = sep.join(request.args)
    log('converse: '+thing)
    load_brain()
    if brain["conversation"] == True and brain["conversation_target"] != request.args["name"]:
        return "reaction:busy"
    if brain["conversation"] == True and brain["conversation_target"] == request.args["name"]:
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args["dialog"], write_file, indent=4)
        return "reaction:thinking"
    if request.args["name"] in brain["social_circle"].keys():
        them = brain["social_circles"][request.args["name"]]
        feeling = them["positive_interaction"] - them["negative_interaction"]
        if feeling < -10:
            return "reaction:ignoring"
        brain["conversation"] = True
        brain["conversation_target"] = request.args["name"]
        brain["social_circles"][request.args["name"]]["last_interaction"] = time.time()
        brain["social_circles"][request.args["name"]]["ip"] = request.args["ip"]
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args, write_file, indent=4)
        save_brain()
        return "reaction:thinking"
    else:
        brain["social_circles"][request.args["name"]] = {
            "positive_interaction": 0,
            "negative_interaction": 0,
            "met": time.time(),
            "last_interaction": time.time(),
            "ip": request.args["ip"]
        }
        brain["conversation"] = True
        brain["conversation_target"] = request.args["name"]
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args["dialog"], write_file, indent=4)
        save_brain()
        return "reaction:thinking"


if __name__ == "__main__":
    log('Starting program in 90 seconds...')
    #time.sleep(90)
    log('Starting.')
    try:
        log('Loading memory...')
        load_memory()
        log('Done.')
    except:
        log("Unexpected error loading memory")
    try:
        log('Loading config...')
        load_config()
        log('Done.')
    except:
        log("Unexpected error loading config")
    # try:
    #     log('Loading neighbors...')
    #     load_neighbors()
    #     log('Done.')
    # except:
    #     log("Unexpected error loading neighbors")
    #     pass
    try:
        log('Running app...')
        app.run(host=args.ip, port=80, debug=True)
    except:
        log("Unexpected error running api")

    # app.run(ssl_context=('/etc/letsencrypt/live/blurrydude.com/fullchain.pem','/etc/letsencrypt/live/blurrydude.com/privkey.pem'), host='192.168.1.51')
