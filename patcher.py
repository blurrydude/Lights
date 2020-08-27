import subprocess
import json
import time
import os
import requests
import os.path
from os import path
from datetime import datetime
import socket

def log(message):
    hasLogDir = path.exists('/home/pi/logs/')
    if hasLogDir == False:
        os.mkdir('/home/pi/logs/')
    logfile = "/home/pi/logs/patcher_log_"+datetime.now().strftime("%Y-%m-%d-%H")+".log"
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
        log('Rebooting.')
        time.sleep(1)
        os.system('sudo shutdown -r now')
        exit()

for i in range(0,5):
    doCheck()