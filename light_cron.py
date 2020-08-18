import subprocess
import json
import time
import os

os.system('cd /home/pi/Lights && git pull --all', shell=True)
time.sleep(10)
datafile = '/home/pi/Lights/lightdata.json'
tokenfile = '/home/pi/lightdata.json'
with open(datafile, "r") as read_file:
    data = json.load(read_file)
hasToken = path.exists(tokenfile)
if hasToken == False:
    with open(tokenfile, "w") as write_file:
        json.dump(data, write_file, sort_keys=True, indent=4)

with open(tokenfile, "r") as read_file:
    token = json.load(read_file)

if token.version != data.version:
    with open(tokenfile, "w") as write_file:
        json.dump(data, write_file, sort_keys=True, indent=4)
    time.sleep(10)
    os.system('reboot')
