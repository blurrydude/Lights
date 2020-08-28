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
personality = {}
intensity = 0
color = (0,0,0)

weather = ["thunderstorms","drizzle","rain","snow","clear weather","cloudy weather","mist","haze","fog"]
colors = ['red','green','blu']
subjects = ["weather","color","time"]

def save_personality():
    with open('/home/pi/personality.json', "w") as write_file:
        json.dump(personality, write_file, indent=4)

def load_personality():
    global personality
    with open('/home/pi/personality.json', "r") as read_file:
        personality = json.load(read_file)

def getSummary():
    summary = 'Your furniture\'s name is '+name+'.\n'+name+' is '
    if personality["activity_level"] < 4:
        summary = summary+'lazy, '
    if personality["activity_level"] >= 4 and personality["activity_level"] < 7:
        summary = summary+'active, '
    if personality["activity_level"] >= 7:
        summary = summary+'hyperactive, '

    if personality["positivity"] < 3:
        summary = summary+'grumpy, '
    if personality["positivity"] >= 3 and personality["positivity"] < 7:
        summary = summary+'even-keeled, '
    if personality["positivity"] >= 7:
        summary = summary+'cheery, '

    if personality["changeability"] < 4:
        summary = summary+'and set in its way.'
    if personality["changeability"] >= 4 and personality["changeability"] < 7:
        summary = summary+'and open-minded.'
    if personality["changeability"] >= 7:
        summary = summary+'and adventurous.'

    summary = summary + '\n'+name+' likes '+personality["likes"]["weather"]
    summary = summary + ', but really thrives in '+personality["superlikes"]["weather"]
    summary = summary + '.\n'+name+' prefers to avoid '+personality["dislikes"]["weather"]
    summary = summary + '.\n'+name+' likes '+colors[personality["likes"]["color"]]+'ish colors, loves '+colors[personality["superlikes"]["color"]]+'ish colors and dislikes '+colors[personality["dislikes"]["color"]]+'ish colors.\n'
    summary = summary + 'Your furniture does its best thinking around '+str(personality["superlikes"]["time"])+':00 or even '+str(personality["likes"]["time"])+':00, but gets lethargic around '+str(personality["dislikes"]["time"])+':00'
    return summary

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
            "ip": args.ip,
            "name": name
        }
        log('Make new config.')
        save_config()

    with open('/home/pi/light_conf.json', "r") as read_file:
        config = json.load(read_file)
        log('Existing config loaded.')
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
    with open('/home/pi/logs/light_server_log_'+datetime.now().strftime("%Y-%m-%d-%H")+'.log', "a+") as write_file:
        write_file.write(message+"\n")

def save_config():
    log('save config')
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
    log('save brain')
    with open('/home/pi/brain.json', "w") as write_file:
        json.dump(brain, write_file, indent=4)

def load_brain():
    log('load brain')
    global brain
    hasbrain = path.exists('/home/pi/brain.json')
    if hasbrain == False:
        save_brain()
    with open('/home/pi/brain.json', "r") as read_file:
        brain = json.load(read_file)

@app.route("/color", methods=["GET"])
def color_endpoint():
    global intensity
    global color
    c = request.args["c"]
    if "dimmer" in c:
        intensity = intensity - 16
    if "brighter" in c:
        intensity = intensity + 16
    if "on" in c:
        intensity = 200
    if "off" in c:
        intensity = 0
    if "full" in c:
        intensity = 255
    if "red" in c:
        color = (1,0,0)
    if "green" in c:
        color = (0,1,0)
    if "blue" in c:
        color = (0,0,1)
    if "orange" in c:
        color = (1,0.25,0)
    if "yellow" in c:
        color = (1,1,0)
    if "magenta" in c:
        color = (1,0,1)
    if "purple" in c:
        color = (1,0,0.25)
    if "cyan" in c:
        color = (0,1,1)
    if "white" in c:
        color = (1,1,1)
    
    intensity = min(max(0, intensity),255)
    r = int(color[0] * intensity)
    g = int(color[1] * intensity)
    b = int(color[2] * intensity)
    while a <= z:
        pixels[a] = (r, g, b)
        mem[a] = (r, g, b)
        a = a + 1
    save_memory(mem)
    return "OK"

@app.route("/reboot", methods=['GET'])
def reboot_endpoint():
    secret = request.args['s']
    if secret == "42":
        os.system('reboot now')

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

@app.route("/log", methods=['GET'])
def log_endpoint():
    page = request.args['p']
    pageFile = open("/home/pi/logs/"+page+"_log_"+datetime.now().strftime("%Y-%m-%d-%H")+".log","r")
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
    #config['lastattention'] = time.time()
    #save_config()
    return mem

@app.route("/config", methods=['GET'])
def config_endpoint():
    config['name'] = name
    return config

@app.route("/brain", methods=['GET'])
def brain_endpoint():
    load_brain()
    return brain

@app.route("/personality", methods=['GET'])
def personality_endpoint():
    load_personality()
    return personality

@app.route("/personalitysummary", methods=['GET'])
def personalitysummary_endpoint():
    load_personality()
    return getSummary()

@app.route("/setautosun", methods=['GET'])
def setautosun_endpoint():
    if request.args['v'] == "True":
        config['autosun'] = True
    if request.args['v'] == "False":
        config['autosun'] = False
    log('set autosun '+str(config['autosun'])+' from '+request.args['v'])
    save_config()
    return config

@app.route("/setpersonality", methods=['GET'])
def setpersonality_endpoint():
    if request.args['v'] == "True":
        config['personality'] = True
    if request.args['v'] == "False":
        config['personality'] = False
    log('set personality '+str(config['personality'])+' from '+request.args['v'])
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
    for k in request.args:
        log(k+": "+request.args[k])
    load_brain()
    if brain["conversation"] == True and brain["conversation_target"] != request.args["name"]:
        return "reaction:busy"
    if brain["conversation"] == True and brain["conversation_target"] == request.args["name"]:
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args, write_file, indent=4)
        return "reaction:thinking"
    if request.args["name"] in brain["social_circle"].keys():
        them = brain["social_circle"][request.args["name"]]
        feeling = them["positive_interaction"] - them["negative_interaction"]
        if feeling < -10:
            return "reaction:ignoring"
        brain["conversation"] = True
        brain["conversation_target"] = request.args["name"]
        brain["social_circle"][request.args["name"]]["last_interaction"] = time.time()
        brain["social_circle"][request.args["name"]]["ip"] = request.args["ip"]
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args, write_file, indent=4)
        save_brain()
        return "reaction:thinking"
    else:
        brain["social_circle"][request.args["name"]] = {
            "positive_interaction": 0,
            "negative_interaction": 0,
            "met": time.time(),
            "last_interaction": time.time(),
            "ip": request.args["ip"]
        }
        brain["conversation"] = True
        brain["conversation_target"] = request.args["name"]
        with open('/home/pi/waiting_dialog.json', "w") as write_file:
            json.dump(request.args, write_file, indent=4)
        save_brain()
        return "reaction:thinking"


if __name__ == "__main__":
    hasLogDir = path.exists('/home/pi/logs/')
    if hasLogDir == False:
        os.mkdir('/home/pi/logs/')
    log('Starting program in 90 seconds...')
    time.sleep(90)
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
