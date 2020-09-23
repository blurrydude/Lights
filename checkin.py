import requests 
import socket
import os
import json
from crontab import CronTab
import urllib

URL = "https://blurrydude.com:5000/checkin"

name = socket.gethostname()
if name == 'pi4in1':
    check_online = urllib.request.urlopen("https://www.google.com").getcode()
    if check_online != 200:
        os.system('sudo reboot now')
        exit()

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
    subjobs = str(job).split('\n')
    for subjob in subjobs:
        if subjob[0] != '#':
            pijobs.append(str(subjob))
for job in root_cron:
    subjobs = str(job).split('\n')
    for subjob in subjobs:
        if subjob[0] != '#':
            rootjobs.append(str(subjob))
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