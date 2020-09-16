import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import neopixel
import board
import json
import os
from os import path
import requests
import argparse
import socket

name = socket.gethostname()

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--ledcount", "-n", help="led count")
args = parser.parse_args()
led_count = int(args.ledcount)

fsacheck = path.exists('/home/pi/fsa.json')
if fsacheck == False:
    response = requests.get('https://blurrydude.com:5000/fsa')
    fsajson = response.text
    with open('/home/pi/fsa.json', 'w') as write_file:
        write_file.write(fsajson)

cred = credentials.Certificate('/home/pi/fsa.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

pixels = neopixel.NeoPixel(board.D18, led_count)
mem = []

last_config_update = datetime.now()
config = {
    "name": name,
    "config_update_frequency_seconds": 60,
    "process_interrupt": 0,
    "private_ip": args.ip,
    "pixels": [],
}
for i in range(led_count):
    config["pixels"].append([0,0,0])

def getRef(path):
    path = path.split('/')
    if len(path) == 2:
        ref = db.collection(path[0]).document(path[1])
    else:
        ref = db.collection(path[0])
    return ref

def load_config():
    global config
    global last_config_update
    now = datetime.now()
    last_config_update = now
    configref = getRef('LightConfig/'+name)
    configdoc = configref.get()
    configdata = configdoc.to_dict()
    if configdata is None:
        configref.set(config)
    else:
        config = configdata

def save_config():
    global config
    configref = getRef('LightConfig/'+name)
    configref.set(config)

def set_pixels():
    global mem
    for i in range(len(config["pixels"])):
        p = config["pixels"][i]
        pixels[i] = (p[0],p[1],p[2])
        mem[i] = p

def has_pixel_update():
    update_pixels = False
    for i in range(len(config["pixels"])):
        p = config["pixels"][i]
        if p != mem[i]:
            update_pixels = True
    

def send_log(message):
    try:
        now = datetime.now()
        if type(message) is object:
            message = json.dumps(message)
        elif type(message) is not str:
            message = str(message)
        print(now.strftime("%Y-%m-%d %H:%M:%S")+': '+message)
        logid = str(now.timestamp())
        entry = {
            "timestamp":now.timestamp(),
            "system_time":now.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }
        getRef('LightConsole_'+name+'/'+logid).set(entry)
    except Exception as e:
        print(e)

load_config()
set_pixels()

while config["process_interrupt"] == 0:
    now = datetime.now()
    try:
        if (now - last_config_update).total_seconds() > config["config_update_frequency_seconds"]:
            load_config()
            do_update = has_pixel_update()
            if do_update == True:
                set_pixels()
    except Exception as e:
        send_log(e)

if config["process_interrupt"] == 3:
    send_log("Process Interrupt 3 - Pull and Reboot")
    os.system("cd /home/pi/Lights && git pull")
    time.sleep(1)
    config["process_interrupt"] = 0
    save_config()
    os.system("sudo reboot now")
elif config["process_interrupt"] == 2:
    send_log("Process Interrupt 2 - Pull and Restart Service")
    os.system("cd /home/pi/Lights && git pull")
    time.sleep(1)
    config["process_interrupt"] = 0
    save_config()
    time.sleep(1)
    os.system("sudo python3 /home/pi/Lights/light_server.py -n "+str(led_count)+" -ip "+args.ip)
elif config["process_interrupt"] == 1:
    send_log("Process Interrupt 1 - Stop Service - WARNING! THIS WILL LEAVE THE PI AT THE TERMINAL WITHOUT REBOOT!")
    time.sleep(1)
    config["process_interrupt"] = 0
    save_config()