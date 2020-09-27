import requests 
import socket
import os
from os import path
import json
from crontab import CronTab
import urllib
import subprocess

# out = subprocess.Popen(['pip3','list'],
#     stdout=subprocess.PIPE,
#     stderr=subprocess.STDOUT)

# stdout,stderr = out.communicate()
# text = str(stdout)
# text = text[2:len(text)-3]
# while "  " in text:
#     text = text.replace('  ',' ')
# lines = text.split('\\n')
# packages = {}
# for line in lines:
#     if "Package" in line or "---" in line:
#         continue
#     data = line.split(' ')
#     packages[data[0]] = data[1]

URL = "https://blurrydude.com:5000/checkin"

name = socket.gethostname()

attempts = 0
if path.exists('/home/pi/checkindata.txt') == False:
    with open('/home/pi/checkindata.txt','w') as write_file:
        write_file.write(str(attempts))
with open('/home/pi/checkindata.txt','r') as read_file:
    attempts = int(read_file.read())
check_online = urllib.request.urlopen("https://www.google.com").getcode()
if check_online != 200:
    if attempts == 1:
        attempts = attempts + 1
        os.system('sudo rfkill block all')
        time.sleep(3)
        os.system('sudo rfkill unblock all')
        time.sleep(3)
    elif attempts >= 5:
        with open('/home/pi/checkindata.txt','w') as write_file:
            write_file.write("0")
        os.system('sudo reboot now')
        exit()
    else:
        attempts = attempts + 1
        with open('/home/pi/checkindata.txt','w') as write_file:
            write_file.write(str(attempts))


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
    #"packages":packages
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