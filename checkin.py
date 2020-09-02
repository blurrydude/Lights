import requests 
import socket
import os
import json
from crontab import CronTab

URL = "https://blurrydude.com:5000/checkin"

name = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
d = s.getsockname()
ip = d[0]
s.close()

pip = requests.get('https://api.ipify.org').text

pi_cron = CronTab('pi')
root_cron = CronTab('root')
pijobs = []
rootjobs = []
rclocal = ""
for job in pi_cron:
    pijobs.append(str(job))
for job in root_cron:
    rootjobs.append(str(job))
with open('/etc/rc.local','r') as read_file:
    lines = read_file.readlines()
    for line in lines:
        if "sudo" in line:
            rclocal = line
data = {
    "publicIp": pip,
    "privateIp": ip,
    "name":name,
    "pijobs":pijobs,
    "rootjobs":rootjobs,
    "rclocal":rclocal
}

PARAMS = {'name':name, 'ip':ip, 'data':json.dumps(data)} 

r = requests.get(url = URL, params = PARAMS)

command = requests.get('https://blurrydude.com:5000/topic?t=commands')
if name.replace('pi','') in command:
    requests.get('https://blurrydude.com:5000/ack?t=commands')
    if "reboot" in command:
        os.system('reboot now')
    else:
        requests.get('http:'+ip+'/command?c='+command)
#  MMFFFFFFFFFLLLSSDDVV
# M - model
# F - device flags
# L - led count
# S - stepper motor count
# D - dc motor count
# V - servo moto count

# var PiModel = {
#     M1A: 0,
#     M1AP: 1,
#     M1B: 2,
#     M1BP: 3,
#     M2B: 4,
#     M2BV12: 5,
#     M3AP: 6,
#     M3B: 7,
#     M3BP: 8,
#     M4B: 9,
#     CM1: 10,
#     CM3: 11,
#     CM3L: 12,
#     CM3P: 13,
#     CM3LP: 14,
#     ZV12: 15,
#     ZV13: 16,
#     ZW: 17
# }

# var DeviceFlags = {
#     HEADLESS: 1,
#     LED_CONTROLLER: 2,
#     FILE_SERVER: 4,
#     WEB_SERVER: 8,
#     RETROPIE: 16,
#     SPOTIFY: 32,
#     WAP: 64,
#     WRT: 128,
#     CNC: 256,
#     OBD: 512,
#     GPS: 1024,
#     SENSOR_TEMP: 2048,
#     SENSOR_HUM: 4096,
#     SENSOR_COLOR: 8192,
#     SENSOR_LIGHT: 16384,
#     CONTROLLER_STEPPER: 32768,
#     CONTROLLER_DCMOTOR: 65536,
#     CONTROLLER_SERVO: 131072,
#     CAMERA: 262144
# }

# var PiModel = {
#     M1A: 0,
#     M1AP: 1,
#     M1B: 2,
#     M1BP: 3,
#     M2B: 4,
#     M2BV12: 5,
#     M3AP: 6,
#     M3B: 7,
#     M3BP: 8,
#     M4B: 9,
#     CM1: 10,
#     CM3: 11,
#     CM3L: 12,
#     CM3P: 13,
#     CM3LP: 14,
#     ZV12: 15,
#     ZV13: 16,
#     ZW: 17
# }
