import time
from datetime import datetime
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(address=0x61)
kit2 = MotorKit()

def setMotorSpeed(motor, speed):
    global direction
    if motor == 1:
        kit2.motor1.throttle = speed
    if motor == 2:
        kit2.motor2.throttle = speed
    if motor == 3:
        kit2.motor3.throttle = speed
    if motor == 4:
        kit2.motor4.throttle = speed


def allStop():
    print('all stop')
    kit2.motor1.throttle = 0
    kit2.motor1.throttle = None
    kit2.motor2.throttle = 0
    kit2.motor2.throttle = None
    kit2.motor3.throttle = 0
    kit2.motor3.throttle = None
    kit2.motor4.throttle = 0
    kit2.motor4.throttle = None

rpm = 30
spm = 200 * rpm
sps = spm / 60
delay = 1 / sps

while True:
   kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
   time.sleep(delay)

# setMotorSpeed(1,1)
# time.sleep(10)
# setMotorSpeed(2,1)
# time.sleep(10)
# allStop()
