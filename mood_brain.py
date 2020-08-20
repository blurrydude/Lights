from datetime import datetime
import time
import random
import socket
import os
from os import path
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--reset", "-reset", help="reset personality")
args = parser.parse_args()

name = socket.gethostname()

config = {}
neighbors = []

personality = {
    "activity_level": 0,
    "changeability": 0,
    "positivity": 0,
    "superlikes": {
        "weather": 0,
        "color": 0,
        "time": 0,
    },
    "likes": {
        "weather": 0,
        "color": 0,
        "time": 0,
    },
    "dislikes": {
        "weather": 0,
        "color": 0,
        "time": 0,
    }
}

brain = {
    "mood": 5,
    "energy": 5,
    "boredom": 0,
    "current_thoughts": [],
    "social_circle": {},
    "last_activity": datetime.now(),
    "last_thought": datetime.now(),
    "last_interaction": datetime.now(),
    "resting": False,
    "conversation": False,
    "conversation_target": "",
    "conversation_rounds": 0
}

weather = ["thunderstorms","drizzle","rain","snow","clear weather","cloudy weather","mist","haze","fog"]
colors = ['red','green','blu']

def save_config():
    with open('/home/pi/light_conf.json', "w") as write_file:
        json.dump(config, write_file, indent=4)

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

def reset_personality():
    makePersonality()
    with open('/home/pi/personality.json', "w") as write_file:
        json.dump(personality, write_file, indent=4)

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

def save_personality():
    with open('/home/pi/personality.json', "w") as write_file:
        json.dump(personality, write_file, indent=4)

def load_personality():
    global personality
    haspersonality = path.exists('/home/pi/personality.json')
    if haspersonality == False:
        makePersonality()
        save_personality()
    with open('/home/pi/personality.json', "r") as read_file:
        personality = json.load(read_file)

def load_neighbors():
    global neighbors
    directory = r'/home/pi/'
    for filename in os.listdir(directory):
        if filename.endswith(".neighbor"):
            f = open(filename, 'r')
            t = f.read()
            f.close()
            neighbors.append(t)

def makePersonality():
    global personality
    personality["activity_level"] = random.randrange(10)+1
    personality["changeability"] = random.randrange(10)+1
    personality["positivity"] = random.randrange(10)+1
    personality["superlikes"]["weather"] = random.choice(weather)
    personality["likes"]["weather"] = random.choice(weather)
    while personality["superlikes"]["weather"] == personality["likes"]["weather"]:
        personality["likes"]["weather"] = random.choice(weather)
    personality["dislikes"]["weather"] = random.choice(weather)
    while personality["superlikes"]["weather"] == personality["dislikes"]["weather"] or personality["likes"]["weather"] == personality["dislikes"]["weather"]:
        personality["dislikes"]["weather"] = random.choice(weather)
        
    personality["superlikes"]["color"] = random.randrange(3)
    personality["likes"]["color"] = random.randrange(3)
    while personality["likes"]["color"] == personality["superlikes"]["color"]:
        personality["likes"]["color"] = random.randrange(3)
        
    personality["dislikes"]["color"] = random.randrange(3)
    while personality["superlikes"]["color"] == personality["dislikes"]["color"] or personality["likes"]["color"] == personality["dislikes"]["color"]:
        personality["dislikes"]["color"] = random.randrange(3)

    personality["superlikes"]["time"] = random.randrange(24)
    timeup = random.randrange(2)
    if timeup == 0:
        timeup = -1
    personality["likes"]["time"] = personality["superlikes"]["time"] + timeup
    oppo = personality["superlikes"]["time"] - 12
    if oppo < 0:
        oppo = 24 + oppo
    personality["dislikes"]["time"] = oppo

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

def processDialog(them, dialog):
    global brain
    context = dialog.split(':')
    dialogType = context[0]
    if dialogType == "topic":
        like = 0
        dislike = 0
        feeling = context[1]
        subject = context[2]
        thought = context[3]
        if personality[feeling][subject] == thought:
            if feeling == "likes":
                like = like + 1
            if feeling == "superlikes":
                like = like + 2
            if feeling == "dislikes":
                like = like + 2
        if feeling == "likes" and personality["superlikes"][subject] == thought:
            like = like + 2
        if feeling == "superlikes" and personality["likes"][subject] == thought:
            like = like + 1
        if feeling == "dislikes" and personality["superlikes"][subject] == thought:
            dislike = dislike + 2
        if feeling == "dislikes" and personality["likes"][subject] == thought:
            dislike = dislike + 1
        

    if dialogType == "reaction":
        reaction = context[1]
        if reaction == "thinking":
            return True
        if reaction == "busy":
            brain["converation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return True
        if reaction == "bye":
            them["positive_interactions"] = them["positive_interactions"] + 1
            brain["converation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return True




def converse():
    global brain
    feelLikeResting = brain["energy"] < 3
    hasdialogwaiting = path.exists('/home/pi/dialog_waiting.json')
    if hasdialogwaiting:
        with open('/home/pi/dialog_waiting.json', "r") as read_file:
            data = json.load(read_file)
        them = brain["social_circle"][data["name"]]
        dialogs = data["dialog"].split(',')
        for dialog in dialogs:
            processDialog(them, dialog)
    
    save_brain()

def rest():
    global brain
    save_brain()

def think():
    global brain
    if brain["conversation"] == True:
        converse()
        return True
    if brain["resting"] == True:
        rest()
        return True
    feelLikeResting = brain["energy"] < 3
    maybeDoSomething = random.randrange(brain["boredom"]) > 3 + (10 - personality["changeability"])
    save_brain()

if args.reset:
    reset_personality()
    time.sleep(1)

load_config()
if config["personality"] == True:
    load_personality()
    load_brain()
    load_neighbors()
    print(config)
    print(personality)
    print(brain)
    print(neighbors)
    think()
else:
    print("personality disabled")