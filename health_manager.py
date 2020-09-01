import os
from os import path
import json
import time
from datetime import datetime

now = datetime.now()

#delete old logs here
mydir = "/home/pi/logs/"
filelist = [ f for f in os.listdir(mydir) if f.endswith(".bak") ]
for f in filelist:
    if datetime.now().strftime("%Y-%m-%d") in f:
        continue
    os.remove(os.path.join(mydir, f))