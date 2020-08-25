import requests
from datetime import datetime

def setPixel(p,r,g,b):
    requests.get('http://192.168.1.236/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(p)+'&z='+str(p))

now = datetime.now()
hour = now.hour
postmeridian = hour > 11
hourColor = (0,255,0)
minuteColor = (0,0,255)
if postmeridian == True:
    hour = hour - 12
    hourColor = (255,0,0)
hourhand = hour * 5
if hourhand == 60:
    hourhand = 0
minutehand = now.minute
if minutehand == hourhand:
    if postmeridian == True:
        setPixel(hourhand,255,0,255)
    else:
        setPixel(hourhand,0,255,255)
else:
    if postmeridian == True:
        setPixel(hourhand,255,0,0)
    else:
        setPixel(hourhand,0,255,0)
    setPixel(minutehand,0,0,255)
if hourhand == 0:
    setPixel(55,0,0,0)
if minutehand == 0:
    setPixel(59,0,0,0)
if hourhand > 0:
    setPixel(hourhand-5,0,0,0)
if minutehand > 0:
    setPixel(minutehand-1,0,0,0)
