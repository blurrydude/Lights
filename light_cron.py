import subprocess
import json
import time
import os
import requests
import os.path
from os import path
from datetime import datetime

def log(message):
    logfile = "/home/pi/light_log_"+datetime.now().strftime("%Y-%m-%d")+".txt"
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    message = date_time + ": " + message
    print(message)
    logFile = open(logfile,"a+")
    logFile.write(message+"\n")
    logFile.close()

def doCheck():
    os.system('cd /home/pi/Lights && git pull --all')
    log('Waiting for ten seconds...')
    time.sleep(10)
    log('Check token')
    datafile = '/home/pi/Lights/lightdata.json'
    tokenfile = '/home/pi/lightdata.json'
    with open(datafile, "r") as read_file:
        data = json.load(read_file)
    log(data['version'])
    hasToken = path.exists(tokenfile)
    if hasToken == False:
        log('Creating new token.')
        with open(tokenfile, "w") as write_file:
            json.dump(data, write_file, sort_keys=True, indent=4)

    with open(tokenfile, "r") as read_file:
        token = json.load(read_file)
    log(token['version'])
    if token['version'] != data['version']:
        with open(tokenfile, "w") as write_file:
            json.dump(data, write_file, sort_keys=True, indent=4)
        log('Waiting ten seconds then rebooting.')
        time.sleep(10)
        os.system('reboot now')
        exit()

for i in range(0,5):
    doCheck()

pis = requests.get('https://blurrydude.com:5000/checkall').text
pip = requests.get('https://api.ipify.org').text

for i in pis:
    s = pis[i].split('|')
    if s[3] == pip:
        with open('/home/pi/'+s[0]+'.neighbor', "w") as write_file:
            json.dump(s, write_file, sort_keys=True, indent=4)
    