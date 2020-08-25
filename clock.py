import requests
from datetime import datetime

def setPixel(p,r,g,b):
    requests.get('http://192.168.1.236/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(p)+'&z='+str(p))

def setRange(a,z,r,g,b):
    requests.get('http://192.168.1.236/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(a)+'&z='+str(z))

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
second = now.second
tick = 0
setRange(0,59,0,0,0)
for i in range(12):
    m = i * 5
    setPixel(m,32,4,0)
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
# if hourhand == 0:
#     setPixel(55,0,0,0)
# if minutehand == 0:
#     setPixel(59,0,0,0)
# if hourhand > 0:
#     setPixel(hourhand-5,0,0,0)
# if minutehand > 0:
#     setPixel(minutehand-1,0,0,0)
lasttick = -1
while ticks < 58:
    if minutehand != tick and hourhand != tick and tick != lasttick:
        if tick == 0:
            setPixel(0,0,4,32)
        elif tick == 5:
            setPixel(5,0,4,32)
        elif tick == 10:
            setPixel(10,0,4,32)
        elif tick == 15:
            setPixel(15,0,4,32)
        elif tick == 20:
            setPixel(20,0,4,32)
        elif tick == 25:
            setPixel(25,0,4,32)
        elif tick == 30:
            setPixel(30,0,4,32)
        elif tick == 35:
            setPixel(35,0,4,32)
        elif tick == 40:
            setPixel(40,0,4,32)
        elif tick == 45:
            setPixel(45,0,4,32)
        elif tick == 50:
            setPixel(50,0,4,32)
        elif tick == 55:
            setPixel(55,0,4,32)
        else:
            setPixel(tick,8,0,16)
        lasttick = tick
    if second != datetime.now().second:
        second = datetime.now().second
        tick = tick + 1