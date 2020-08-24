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
parser.add_argument("--fast", "-f", help="speed up the iterator for this instance")
parser.add_argument("--continuous", "-c", help="continuous running")
args = parser.parse_args()

name = socket.gethostname()

config = {}
neighbors = []
mem = []

segments = [
    {"start": 0, "end": 5},
    {"start": 6, "end": 11},
    {"start": 12, "end": 17},
    {"start": 18, "end": 24},
    {"start": 25, "end": 30},
    {"start": 31, "end": 35},
    {"start": 36, "end": 39},
    {"start": 40, "end": 50},
    {"start": 51, "end": 56},
    {"start": 57, "end": 67},
    {"start": 68, "end": 71},
    {"start": 72, "end": 76},
    {"start": 77, "end": 82},
    {"start": 83, "end": 89},
    
    {"start": 90, "end": 94},
    {"start": 95, "end": 104},
    {"start": 105, "end": 109},
    {"start": 110, "end": 119}
]

sections = [
    [7,8,9], #head
    [6, 10], #heart
    [5, 11], #shelf 1
    [4, 12], #shelf 2
    [3, 13], #shelf 3
    [2,1,0], #shelf 4
    [14], #bottom
    [15], #inside
    [16], #top
    [17]  #outside
]

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

def save_memory(memory):
    with open('/home/pi/light_mem.json', "w") as write_file:
        json.dump(memory, write_file, indent=4)

def load_memory():
    global mem
    hasMem = path.exists('/home/pi/light_mem.json')
    if hasMem == False:
        for i in range(120):
            mem.append((0,0,0))
        save_memory(mem)
    try:
        with open('/home/pi/light_mem.json', "r") as read_file:
            mem = json.load(read_file)
        return mem
    except:
        for i in range(120):
            mem.append((0,0,0))
        os.remove('/home/pi/light_mem.json')
        with open('/home/pi/light_mem.json', "w") as write_file:
            json.dump(mem, write_file, indent=4)

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
    brain["boredom"] = min(10,max(0,brain["boredom"]))
    brain["mood"] = min(10,max(0,brain["mood"]))
    brain["energy"] = min(10,max(0,brain["energy"]))
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
                brain["boredom"] = max(brain["boredom"] - 1, 0)
            if feeling == "dislikes":
                reply = "reaction:veryhappy"
                brain["boredom"] = max(brain["boredom"] - 1, 0)
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
            brain["boredom"] = min(brain["boredom"] + 1, 10)
        if feeling == "dislikes" and personality["likes"][subject] == thought:
            dislike = dislike + 1
            if personality["positivity"] < 4:
                dislike = dislike + 1
            reply = "reaction:mad"
            brain["boredom"] = min(brain["boredom"] + 1, 10)
        them["positive_interaction"] = them["positive_interaction"] + like
        them["negative_interaction"] = them["negative_interaction"] + dislike
        save_brain()
        return reply

    if dialogType == "reaction":
        reaction = context[1]
        if reaction == "thinking" or reaction == "neutral":
            return ""
        if reaction == "happy":
            them["positive_interaction"] = them["positive_interaction"] + 1
            return ""
        if reaction == "veryhappy":
            them["positive_interaction"] = them["positive_interaction"] + 1
            them["negative_interaction"] = them["negative_interaction"] - 1
            return ""
        if reaction == "mad":
            them["negative_interaction"] = them["negative_interaction"] + 1
            return ""
        if reaction == "verymad":
            them["negative_interaction"] = them["negative_interaction"] + 1
            them["positive_interaction"] = them["positive_interaction"] - 1
            return ""
        if reaction == "busy":
            brain["conversation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""
        if reaction == "bye":
            them["positive_interaction"] = them["positive_interaction"] + 1
            brain["conversation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""
        if reaction == "ignoring":
            them["negative_interaction"] = them["negative_interaction"] + 1
            brain["conversation"] = False
            brain["conversation_target"] = ""
            save_brain()
            return ""

def converse():
    global brain
    load_memory()
    print('conversing')
    hasdialogwaiting = path.exists('/home/pi/waiting_dialog.json')
    if len(neighbors) == 0:
        print('no neighbors')
        brain["conversation_rounds"] = brain["conversation_rounds"] + 1
        return
    if hasdialogwaiting == False:
        print('no dialog waiting')
        brain["conversation_rounds"] = brain["conversation_rounds"] + 1
        return
    replies = []
    with open('/home/pi/waiting_dialog.json', "r") as read_file:
        data = json.load(read_file)
    them = brain["social_circle"][data["name"]]
    dialogs = data["dialog"].split(',')
    for dialog in dialogs:
        replies.append(processDialog(them, dialog))
    feelLikeResting = brain["energy"] < 3
    bored = random.randrange(brain["boredom"]) > 3 + (10 - personality["activity_level"])
    if feelLikeResting == True or bored == True or brain["conversation_rounds"] > (10-personality["activity_level"] + personality["positivity"] + brain["mood"]):
        brain["conversation"] = False
        brain["conversation_target"] = ""
        brain["conversation_rounds"] = 0
        replies.append("reaction:bye")
    else:
        feelingChoices = ["superlikes","likes","dislikes"]
        if personality["positivity"] < 4:
            feelingChoices = ["likes","dislikes"]
        if personality["positivity"] >= 7:
            feelingChoices = ["superlikes","likes"]
        feeling = random.choice(feelingChoices)
        subject = random.choice(subjects)
        thought = personality[feeling][subject]
        replies.append("topic:"+feeling+":"+subject+":"+thought)

    print(replies)
    sep = ','
    send = sep.join(replies)

    response = requests.get("http://"+data["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog="+send)
    os.remove('/home/pi/waiting_dialog.json')
    processDialog(them, response.text)
    brain["conversation_rounds"] = brain["conversation_rounds"] + 1

    brain["energy"] = max(brain["energy"] - 1, 0)
    save_brain()

def rest():
    global brain
    print('resting')
    brain["energy"] = min(brain["energy"] + 1, 10)
    if brain["energy"] == 10:
        brain["resting"] = False
    if percentChance(50) == True:
        brain["boredom"] = min(brain["boredom"] + 1, 10)
    save_brain()

def percentChance(percent):
    return random.randrange(100) < percent

def setHead(r,g,b):
    section = sections[0]
    for s in section:
        segment = segments[s]
        requests.get('http://'+config["ip"]+'/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(segment["start"])+'&z='+str(segment["end"]))

def updateMoodLights():
    section = sections[1]
    r = brain["mood"]*25
    b = (10 - brain["mood"])*25
    for s in section:
        segment = segments[s]
        requests.get('http://'+config["ip"]+'/?r='+str(r)+'&g=0&b='+str(b)+'&a='+str(segment["start"])+'&z='+str(segment["end"]))

def think():
    global brain
    if brain["conversation"] == True:
        setHead(0,200,0) 
        return converse()
    if brain["resting"] == True:
        setHead(0,60,200)
        return rest()
    print('thinking...')
    feelLikeResting = brain["energy"] < 3
    bored = random.randrange(brain["boredom"]+1) > 3 + (10 - personality["activity_level"])
    if feelLikeResting == True:
        print('I do feel a bit tired')
        if percentChance(personality["activity_level"]*2):
            brain["boredom"] - 1
        brain["resting"] = True
        setHead(0,60,200)
        return rest()
    bored = random.randrange(brain["boredom"]+1) > 3 + (10 - personality["activity_level"])
    if bored:
        print('I am quite bored')
        if percentChance(personality["positivity"]*10):
            setHead(200,60,0)
            print('Think I might reach out to someone, but who?')
            if len(brain["social_circle"]) > 0:
                print('Maybe a friend...')
                talkton = random.choice(neighbors)
                if talkton["name"] in brain["social_circle"].keys():
                    talkto = brain["social_circle"][talkton["name"]]
                    rep = requests.get("http://"+talkto["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog=topic:likes:weather:"+personality["likes"]["weather"])
                    brain["conversation"] = True
                    brain["conversation_target"] = talkto["name"]
                    print('I\'ll chat up '+brain["conversation_target"])
                    processDialog(talkto, rep.text)
                    return
                print('can\'t seem to find any of my friends\' numbers...')
                if percentChance(10):
                    brain["mood"] = max(0,brain["mood"] - 1)
                    updateMoodLights()
            if len(neighbors) > 0:
                print('Maybe a neighbor...')
                talkto = random.choice(neighbors)
                if "ip" not in talkto.keys():
                    print('this is unexpected...')
                    print(talkto)
                rep = requests.get("http://"+talkto["ip"]+"/converse?name="+name+"&ip="+config["ip"]+"&dialog=topic:likes:weather:"+personality["likes"]["weather"])
                brain["conversation"] = True
                brain["conversation_target"] = talkto["name"]
                print('I\'ll chat up '+brain["conversation_target"])
                brain["social_circle"][talkto["name"]] = {
                    "positive_interaction": 0,
                    "negative_interaction": 0,
                    "met": time.time(),
                    "last_interaction": time.time(),
                    "ip": talkto["ip"]
                }
                processDialog(brain["social_circle"][talkto["name"]], rep.text)
                return
        elif percentChance(personality["changeability"]*10):
            print('A new look, that\'s what\'s needed here.')
            setHead(200,0,60)
            rx = 8
            gx = 8
            bx = 8

            if personality["superlikes"]["color"] == 0:
                while gx == rx or gx == bx:
                    rx = rx + random.randrange(1,9)
            if personality["superlikes"]["color"] == 1:
                while gx == rx or gx == bx:
                    gx = gx + random.randrange(1,9)
            if personality["superlikes"]["color"] == 2:
                while bx == rx or gx == bx:
                    bx = bx + random.randrange(1,9)
            if personality["likes"]["color"] == 0:
                while gx == rx or rx == bx:
                    rx = rx + random.randrange(0,5)
            if personality["likes"]["color"] == 1:
                while gx == rx or gx == bx:
                    gx = gx + random.randrange(0,5)
            if personality["likes"]["color"] == 2:
                while bx == rx or gx == bx:
                    bx = bx + random.randrange(0,5)
            r = min(255,rx*16)
            g = min(255,gx*16)
            b = min(255,bx*16)
            sec = random.randrange(2,6) #bottom 4 shelves
            for s in sections[sec]:
                segment = segments[s]
                requests.get('http://'+config["ip"]+'/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(segment["start"])+'&z='+str(segment["end"]))
                rd = random.randrange(3)
                time.sleep(rd)
            r = min(255,random.randrange(2,8+1)*32)
            g = min(255,random.randrange(2,8+1)*32)
            b = min(255,random.randrange(2,8+1)*32)
            sec = random.randrange(6,10) #plume
            for s in sections[sec]:
                segment = segments[s]
                requests.get('http://'+config["ip"]+'/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(segment["start"])+'&z='+str(segment["end"]))
                rd = random.randrange(3)
                time.sleep(rd)
            brain["boredom"] = max(0,brain["boredom"] - (11 - personality["activity_level"]))
            setHead(255,0,0)
            return
    if bored:
        brain["mood"] = max(brain["mood"] - 1, 0)
    else:
        brain["mood"] = min(brain["mood"] + 1, 10)
    print('My mood is '+str(brain["mood"]))
    setHead(255,0,0)
    updateMoodLights()
    if percentChance(personality["activity_level"]*8):
        brain["boredom"] = min(brain["boredom"] + 1, 10)
    if percentChance((10 - personality["activity_level"])*10):
        brain["energy"] = max(brain["energy"] - 1, 0)
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
    delay = 15
    if args.fast and bool(args.fast) == True:
        print('going fast')
        delay = 1
    if args.continuous and bool(args.continuous) == True:
        print('Ctrl+C to stop')
        while True:
            think()
            time.sleep(delay)
    else:
        for i in range(3):
            think()
            time.sleep(delay)

else:
    print("personality disabled")