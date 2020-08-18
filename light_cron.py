import subprocess
import json
import time
import os

os.system('cd /home/pi/Lights && git pull --all')
print('Waiting for ten seconds...')
time.sleep(10)
print('Check token')
datafile = '/home/pi/Lights/lightdata.json'
tokenfile = '/home/pi/lightdata.json'
with open(datafile, "r") as read_file:
    data = json.load(read_file)
print(data)
hasToken = path.exists(tokenfile)
if hasToken == False:
    with open(tokenfile, "w") as write_file:
        json.dump(data, write_file, sort_keys=True, indent=4)

with open(tokenfile, "r") as read_file:
    token = json.load(read_file)
print(token)
if token.version != data.version:
    with open(tokenfile, "w") as write_file:
        json.dump(data, write_file, sort_keys=True, indent=4)
    print('Waiting ten seconds then rebooting.')
    time.sleep(10)
    os.system('reboot')
