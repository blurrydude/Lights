from datetime import datetime
import time
import random
import socket
import os
from os import path
import json
import argparse
import requests

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
    "last_activity": time.time(),
    "last_thought": time.time(),
    "last_interaction": time.time(),
    "resting": False,
    "conversation": False,
    "conversation_target": "",
    "conversation_rounds": 0
}

weather = ["thunderstorms","drizzle","rain","snow","clear weather","cloudy weather","mist","haze","fog"]
colors = ['red','green','blu']
subjects = ["weather","color","time"]

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
            f = open("/home/pi/"+filename, 'r')
            t = f.read()
            f.close()
            a = json.loads(t)
            neighbors.append({
                "name":a[0],
                "ip":a[2],
                "pip":a[3]
            })

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
        reply = "reaction:neutral"
        if personality[feeling][subject] == thought:
            if feeling == "likes":
                like = like + 1
                reply = "reaction:happy"
            if feeling == "superlikes":
                like = like + 1
                if personality["positivity"] >= 7:
                    like = like + 1
                reply = "reaction:veryhappy"
                brain["boredom"] = min(brain["boredom"] - 1, 0)
            if feeling == "dislikes":
                reply = "reaction:veryhappy"
                brain["boredom"] = min(brain["boredom"] - 1, 0)
                like = like + 1
                if personality["positivity"] < 7:
                    like = like + 1
        if feeling == "likes" and personality["superlikes"][subject] == thought:
            like = like + 1
            reply = "reaction:happy"
        if feeling == "superlikes" and personality["likes"][subject] == thought:
            like = like + 1
            if personality["positivity"] >= 7:
                like = like + 1
            reply = "reaction:happy"
        if feeling == "dislikes" and personality["superlikes"][subject] == thought:
            dislike = dislike + 1
            if personality["positivity"] < 7:
                dislike = dislike + 1
            reply = "reaction:verymad"
            brain["boredom"] = max(brain["boredom"] + 1, 10)
        if feeling == "dislikes" and personality["likes"][subject] == thought:
            dislike = dislike + 1
            if personality["positivity"] < 4:
                dislike = dislike + 1
            reply = "reaction:mad"
            brain["boredom"] = max(brain["boredom"] + 1, 10)
        them["positive_interactions"] = them["positive_interactions"] + like
        them["negative_interactions"] = them["negative_interactions"] + dislike
        save_brain()
        return reply

    if dialogType == "reaction":
        reaction = context[1]
        if reaction == "thinking" or reaction == "neutral":
            return ""
        if reaction == "happy":
            them["positive_interactions"] = them["positive_interactions"] + 1
            return ""
        if reaction == "veryhappy":
            them["positive_interactions"] = them["positive_interactions"] + 1
            them["negative_interactions"] = them["negative_interactions"] - 1
            return ""
        if reaction == "mad":
            them["negative_interactions"] = them["negative_interactions"] + 1
            return ""
        if reaction == "verymad":
            them["negative_interactions"] = them["negative_interactions"] + 1
            them["positive_interactions"] = them["positive_interactions"] - 1
            return ""
        if reaction == "busy":
            brain["converation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""
        if reaction == "bye":
            them["positive_interactions"] = them["positive_interactions"] + 1
            brain["converation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""
        if reaction == "ignoring":
            them["negative_interactions"] = them["negative_interactions"] + 1
            brain["converation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""

def converse():
    global brain
    print('conversing')
    hasdialogwaiting = path.exists('/home/pi/dialog_waiting.json')
    if len(neighbors) == 0:
        return
    if hasdialogwaiting == False:
        return
    replies = []
    with open('/home/pi/dialog_waiting.json', "r") as read_file:
        data = json.load(read_file)
    them = brain["social_circle"][data["name"]]
    dialogs = data["dialog"].split(',')
    for dialog in dialogs:
        replies.append(processDialog(them, dialog))
    feelLikeResting = brain["energy"] < 3
    bored = random.randrange(brain["boredom"]) > 3 + (10 - personality["activity_level"])
    if feelLikeResting == True or bored == True:
        brain["conversation"] = False
        brain["conversation_target"] = ""
        replies.append("reaction:bye")
    else:
        feelingChoices = ["superlikes","likes","dislikes"]
        if personality["positivity"] < 4:
            feelingChoices = ["likes","dislikes"]
        if personality["positivity"] >= 7:
            feelingChoices = ["superlikes","likes"]
        feeling = random.choice(feelingChoices)
        subject = random.choice(subjects)
        thought = brain[feeling][subject]
        replies.append("topic:"+feeling+":"+subject+":"+thought)
    sep = ','
    send = sep.join(replies)

    response = requests.get("http://"+data["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog="+send)
    processDialog(them, response.text)

    brain["energy"] = min(brain["energy"] - 1, 0)
    save_brain()

def rest():
    global brain
    print('resting')
    brain["energy"] = max(brain["energy"] + 1, 10)
    if brain["energy"] == 10:
        brain["resting"] = False
    brain["boredom"] = max(brain["boredom"] + 1, 10)
    save_brain()

def percentChance(percent):
    return random.randrange(100) < percent

def think():
    global brain
    if brain["conversation"] == True:
        return converse()
    if brain["resting"] == True:
        return rest()
    feelLikeResting = brain["energy"] < 3
    bored = random.randrange(brain["boredom"]+1) > 3 + (10 - personality["activity_level"])
    if feelLikeResting == True:
        if percentChance(personality["activity_level"]*2):
            brain["boredom"] - 1
        brain["resting"] = True
        return
    bored = random.randrange(brain["boredom"]+1) > 3 + (10 - personality["activity_level"])
    if bored:
        if percentChance(personality["positivity"]*10):
            if len(brain["social_circle"]) > 0:
                print('talk to a known acquaintance, if we like them')
                talkto = random.choice(brain["social_circle"])
                rep = requests.get("http://"+talkto["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog=topic:likes:weather:"+personality["likes"]["weather"])
                brain["conversation"] = True
                brain["conversation_target"] = talkto["name"]
                processDialog(talkto, rep.text)
                return
            if len(neighbors) > 0:
                print('pick a neighbor to try to befriend')
                talkto = random.choice(neighbors)
                rep = requests.get("http://"+talkto["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog=topic:likes:weather:"+personality["likes"]["weather"])
                brain["conversation"] = True
                brain["conversation_target"] = talkto["name"]
                brain["social_circles"][talkto["name"]] = {
                    "positive_interaction": 0,
                    "negative_interaction": 0,
                    "met": time.time(),
                    "last_interaction": time.time(),
                    "ip": talkto["ip"]
                }
                processDialog(brain["social_circles"][talkto["name"]], rep.text)
                return
        elif percentChance(personality["changeability"]*10):
            print('change display and plume colors')
            return

    if percentChance((10 - personality["activity_level"])*5):
        brain["boredom"] = max(brain["boredom"] + 1, 10)
    if percentChance((10 - personality["activity_level"])*10):
        brain["energy"] = min(brain["energy"] - 1, 0)
    save_brain()

if args.reset:
    reset_personality()
    time.sleep(1)

load_config()
if config["personality"] == True:
    load_personality()
    load_brain()
    load_neighbors()
    print("\n--------------------------------config--------------------------------\n")
    print(json.dumps(obj=config,indent=4))
    print("\n--------------------------------personality--------------------------------\n")
    print(json.dumps(obj=personality,indent=4))
    print("\n--------------------------------brain--------------------------------\n")
    print(json.dumps(obj=brain,indent=4))
    print("\n--------------------------------neighbors--------------------------------\n")
    print(json.dumps(obj=neighbors,indent=4))
    think()
else:
    print("personality disabled")