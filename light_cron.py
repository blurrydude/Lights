import subprocess
import json
import time
import os
import requests
import os.path
from os import path
from datetime import datetime
import socket

config = {}
pip = requests.get('https://api.ipify.org').text

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
    else:
        with open('/home/pi/light_conf.json', "r") as read_file:
            config = json.load(read_file)

def getWeatherData():
    key = 'd7859f3f349211398b8415df8f05633f'
    r = requests.get(url = "https://api.openweathermap.org/data/2.5/weather", params = {'lat':config['lat'], 'lon':config['lon'], 'appid':key, 'units':'imperial'})
    with open("/home/pi/weather.json", "w") as write_file:
        json.dump(r.json(), write_file, sort_keys=True, indent=4)

def log(message):
    logfile = "/home/pi/light_cron_log_"+datetime.now().strftime("%Y-%m-%d-%H")+".log"
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    message = date_time + ": " + message
    print(message)
    logFile = open(logfile,"a+")
    logFile.write(message+"\n")
    logFile.close()

def doCheck():
    log('Check for neighbors...')

    pis = json.loads(requests.get('https://blurrydude.com:5000/checkall').text)

    name = socket.gethostname()
    for i in pis:
        s = i.split('|')
        if s[3] == pip and s[0]+'' != name+'':
            if path.exists('/home/pi/'+s[0]+'.neighbor') == False:
                log('Found a new neighbor at '+s[2])
            with open('/home/pi/'+s[0]+'.neighbor', "w") as write_file:
                json.dump(s, write_file, sort_keys=True, indent=4)

load_config()
getWeatherData()
doCheck()