import requests
import time
import threading

colors = [
    [255,255,255],
    [255,  0,  0],
    [  0,255,  0],
    [  0,  0,255],
    [  0,255,255],
    [255,  0,255],
    [255,255,  0],
    [128,  0,255],
    [255,128,  0],
    [  0,255,128],
    [255,  0,128],
    [128,255,  0],
    [  0,128,255]
]
time.sleep(10)
def doThing1(c):
    time.sleep(0.01)
    requests.get('http://192.168.1.234/?r='+str(c[0])+'&g='+str(c[1])+'&b='+str(c[2])+'&a=0&z=119')
def doThing2(c):
    requests.get('http://192.168.1.226/?r='+str(c[0])+'&g='+str(c[1])+'&b='+str(c[2])+'&a=0&z=119')

while True:
    for c in colors:
        #c = colors[color]
        t1 = threading.Thread(target=doThing1,args=[c])
        t2 = threading.Thread(target=doThing2,args=[c])
        t1.start()
        t2.start()
        time.sleep(5)