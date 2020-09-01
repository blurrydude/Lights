import pifacedigitalio as p
import time
p.init()
p.digital_write(0,1)
time.sleep(10)
p.digital_write(0,0)