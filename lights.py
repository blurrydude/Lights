#! /usr/bin/env python3
from evdev import InputDevice, categorize, ecodes
import board
import neopixel
import time
import argparse
import os
import os.path
from os import path
import random
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--mode", "-m", help="static, range, chase, ui or controller. default:static")
parser.add_argument("--color", "-c", help="white, red, green, blue, magenta, cyan, yellow, default: white")
parser.add_argument("--intensity", "-i", help="0 - 255, default: 255")
parser.add_argument("--speed", "-s", help="chase mode only. nths of a second between update, default: 32")
parser.add_argument("--loops", "-l", help="chase mode only. times to chase, default: 10")
parser.add_argument("--rangestart", "-a", help="chase or range mode only. Start of range of LEDs, default:0")
parser.add_argument("--rangeend", "-b", help="chase or range mode only. End of range of LEDs, defaults to max number of LEDs")
parser.add_argument("--endstate", "-o", help="chase mode only. 0 - 255 intensity of white light after loops. default:0")
parser.add_argument("--ledcount", "-n", help="Number of LEDs. default:50")
args = parser.parse_args()

led_count = 50
intensity = 255
speed = 32
loops = 10
start = 0
end = led_count
mode = "static"
endstate = 0
colorWord = "white"
if args.color:
    colorWord = args.color
if args.endstate:
    endstate = int(args.endstate)
if args.mode:
    mode = args.mode
if args.rangestart:
    start = int(args.rangestart)
if args.rangeend:
    end = int(args.rangeend)
if args.speed and int(args.speed) > 0:
    speed = int(args.speed)
if args.loops and int(args.loops) > 0:
    loops = int(args.loops)
if args.intensity:
    intensity = args.intensity
if args.ledcount:
    led_count = int(args.ledcount)

pixels = neopixel.NeoPixel(board.D18, led_count)

def initWhite(l):
    for x in range(led_count):
        pixels[x] = (l,l,l)

def initColor(r,g,b):
    for x in range(led_count):
        pixels[x] = (r,g,b)

def doChase(col, spd, loops, start, end):
    for loop in range(loops):
        for head in range(led_count+8):
            if head >= start and head <= end+8:
                tail = head - 8
                if head < min(led_count,end):
                    pixels[head] = col
                if tail > -1 and tail <= min(led_count,end+8):
                    pixels[tail] = (0,0,0)
                time.sleep((1/int(spd)))

def doOn(col, start, end):
    for x in range(led_count):
        if x >= start and x <= end:
            pixels[x] = col

def selectColor(c, i):
    i = int(i)
    color = (i,i,i)
    if c == "red":
        color = (i,0,0)
    if c == "green":
        color = (0,i,0)
    if c == "blue":
        color = (0,0,i)
    if c == "magenta":
        color = (i,0,i)
    if c == "cyan":
        color = (0,i,i)
    if c == "yellow":
        color = (i,i,0)
    return color

def doUI():
    running = True
    while running == True:
        print("MAIN MENU ----------------")
        print("0 - Exit Program")
        print("1 - Set LED Count")
        print("2 - Set Frame Delay")
        print("3 - Chase")
        print("4 - Set All")
        print("5 - Set Range")
        print("6 - Display Config")
        print("7 - Morse Code")
        command = int(input("Please enter a numeric choice: "))

        os.system('clear')
        if command == 0:
            exit()
        if command == 1:
            doSetLedCountPrompt()
        if command == 2:
            doSetFrameDelayPrompt()
        if command == 3:
            doChasePrompt()
        if command == 4:
            doSetAllPrompt()
        if command == 5:
            doSetRangePrompt()
        if command == 6:
            doDisplayConfig()
        if command == 7:
            doMorsePrompt()

def doSetLedCountPrompt():
    global led_count
    global pixels
    print("SET LED COUNT ------------")
    response = input("Please enter the number of LEDs in the string [enter:50]: ") or "50"
    led_count = int(response)
    pixels = neopixel.NeoPixel(board.D18, led_count)
    
def doSetFrameDelayPrompt():
    global speed
    print("SET FRAME DELAY ----------")
    response = input("Please enter the delay between LED updates in fractions of a second (1/n) [enter:16]: ") or "16"
    speed = int(response)

def doChasePrompt():
    print("CHASE --------------------")
    icolor = input("Color (white,red,blue,green,yellow,cyan,magenta): ")
    iintensity = int(input("Intensity (0-255) [enter:8]: ") or "8")
    iloops = int(input("Loops (1+) [enter:10]: ") or "10")
    iafter = int(input("After intensity (0-255) [enter:0]: ") or "0")
    istart = int(input("Starting LED (0 to one less than total count) [enter:0]: ") or "0")
    iend = int(input("Ending LED (0 to one less than total count, 0 to default to end of string) [enter:0]: ") or "0")
    if iend == 0:
        iend = led_count - 1
    icolorB = selectColor(icolor, iintensity)
    doChase(icolorB, speed, iloops, istart, iend)
    initWhite(iafter)

def doSetAllPrompt():
    print("SET ALL LEDS -------------")
    icolor = input("Color (white,red,blue,green,yellow,cyan,magenta): ")
    iintensity = int(input("Intensity (0-255) [enter:0]: ") or "0")
    icolorB = selectColor(icolor, iintensity)
    doOn(icolorB, 0, led_count)

def doSetRangePrompt():
    print("SET LED RANGE ------------")
    icolor = input("Color (white,red,blue,green,yellow,cyan,magenta) [enter:white]: ")
    iintensity = int(input("Intensity (0-255) [enter:0]: ") or "0")
    istart = int(input("Starting LED (0 to one less than total count) [enter:0]: ") or "0")
    iend = int(input("Ending LED (0 to one less than total count, 0 to default to end of string) [enter:0]: ") or "0")
    if iend == 0:
        iend = led_count - 1
    icolorB = selectColor(icolor, iintensity)
    doOn(icolorB, istart, iend)
    
def doDisplayConfig():
    print(str(led_count) + " LEDs --- 1/"+str(speed)+" second LED update delay")
    print("--------------------------")

def doMorsePrompt():
    print("SET LED RANGE ------------")
    icolor = input("Color (white,red,blue,green,yellow,cyan,magenta) [enter:white]: ")
    iintensity = int(input("Intensity (0-255) [enter:0]: ") or "0")
    istart = int(input("Starting LED (0 to one less than total count) [enter:0]: ") or "0")
    iend = int(input("Ending LED (0 to one less than total count, 0 to default to end of string) [enter:0]: ") or "0")
    imessage = input("Please enter the message to encode: ")
    if iend == 0:
        iend = led_count - 1
    icolorB = selectColor(icolor, iintensity)
    doMorse(imessage,icolorB,istart,iend)

def doMorse(message, color, start, end):
    message = message.lower()
    morse_message = ""
    for i in range(len(message)):
        c = message[i]
        morse_message = morse_message + getMorseChar(c)
    for x in range(led_count):
        morse_message = morse_message + "0"
    #doMorseMessage(morse_message,color,start,end)
    doMorseStreaming(morse_message,color,start,end)

def getMorseChar(c):
    if c == " ":
        return "00"
    if c == ".":
        return "000"
    if c == "a":
        return "120"
    if c == "b":
        return "21110"
    if c == "c":
        return "21210"
    if c == "d":
        return "2110"
    if c == "e":
        return "10"
    if c == "f":
        return "11210"
    if c == "g":
        return "2210"
    if c == "h":
        return "11110"
    if c == "i":
        return "110"
    if c == "j":
        return "12220"
    if c == "k":
        return "2120"
    if c == "l":
        return "12110"
    if c == "m":
        return "220"
    if c == "n":
        return "210"
    if c == "o":
        return "2220"
    if c == "p":
        return "12210"
    if c == "q":
        return "22120"
    if c == "r":
        return "1210"
    if c == "s":
        return "1110"
    if c == "t":
        return "20"
    if c == "u":
        return "1120"
    if c == "v":
        return "11120"
    if c == "w":
        return "1220"
    if c == "x":
        return "21120"
    if c == "y":
        return "21220"
    if c == "z":
        return "22110"
    if c == "1":
        return "122220"
    if c == "2":
        return "112220"
    if c == "3":
        return "111220"
    if c == "4":
        return "111120"
    if c == "5":
        return "111110"
    if c == "6":
        return "211110"
    if c == "7":
        return "221110"
    if c == "8":
        return "222110"
    if c == "9":
        return "222210"
    if c == "0":
        return "222220"

def doMorseMessage(morse, icolor, start, end):
    for i in range(len(morse)):
        d = int(morse[i])
        if d == 0:
            time.sleep(1)
        if d == 1:
            doOn(icolor, start, end)
            time.sleep(0.1)
            doOn((0,0,0), start, end)
        if d == 2:
            doOn(icolor, start, end)
            time.sleep(0.4)
            doOn((0,0,0), start, end)
        time.sleep(0.1)

def doMorseStreaming(morse, icolor, start, end):
    global speed
    original_speed = speed
    speed = 1000
    stack = []
    length = end - start
    # for x in range(length):
    #     stackAndShift(0)
    for i in range(len(morse)):
        d = int(morse[i])
        if d == 0:
            stackAndShift(0)
            stackAndShift(0)
            stackAndShift(0)
            stackAndShift(0)
            stackAndShift(0)
            stackAndShift(0)
        if d == 1:
            stackAndShift(1)
        if d == 2:
            stackAndShift(1)
            stackAndShift(1)
            stackAndShift(1)
            stackAndShift(1)
        stackAndShift(0)
        stackAndShift(0)
        stackAndShift(0)
    
    for x in range(length):
        stackAndShift(0)

    # s = 0
    # while s < len(stack)-length:
    #     for x in range(length):
    #         p = x + start
    #         t = x + s
    #         if stack[t] == 1:
    #             pixels[p] = icolor
    #         if stack[t] == 0:
    #             pixels[p] = (0,0,0)
    #     s = s + 1
        #time.sleep(1/int(speed))
    speed = original_speed

def stackAndShift(bit):
    p = led_count - 1
    while p > 0:
        pixels[p] = pixels[p-1]
        p = p - 1
    if bit == 0:
        pixels[0] = (0,0,0)
    if bit == 1:
        pixels[0] = (255,255,255)

def doTwinkle(inten):
    brightness = int(inten/16)
    if brightness < 1:
        brightness = 1
    startTwinkle = datetime.datetime.now()
    while (datetime.datetime.now()-startTwinkle).total_seconds() < 60:
        #brightness = random.randint(0,16) + 1
        red = random.randint(0,16) * brightness
        green = random.randint(0,16) * brightness
        blue = random.randint(0,16) * brightness
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        color = (red, green, blue)
        pixel = random.randint(0, led_count-1)
        delay = random.randint(1,70)
        pixels[pixel] = color
        time.sleep(delay*0.01)

def doController():
    gamepad = InputDevice('/dev/input/event0')
    print(gamepad)
    color = [1,0,0]
    xintensity = 16
    hasConfig = path.exists('lights.conf')
    in_menu = False
    menu_data = 0
    escaping_menu = False
    startCount = 0
    previous_intensity = 0
    previous_color = [1,1,1]
    if hasConfig == False:
        configFile = open("lights.conf","w")
        configFile.write("0|1|0|64")
        configFile.close()
        doChase((16,0,0), 256, 3, 0, led_count-1)
    if hasConfig == True:
        configFile = open("lights.conf","r")
        configData = configFile.read()
        conf = configData.split("|")
        color = [int(conf[0]),int(conf[1]),int(conf[2])]
        xintensity = int(conf[3])
        configFile.close()
        doChase((0,16,0), 256, 3, 0, led_count-1)
    initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
    #evdev takes care of polling the controller in a loop
    for event in gamepad.read_loop():
        if in_menu == True:
            if xintensity == 0:
                xintensity = 8
            red = getColor("red",xintensity)
            green = getColor("green",xintensity)
            blue = getColor("blue",xintensity)
            cyan = getColor("cyan",xintensity)
            magenta = getColor("magenta",xintensity)
            yellow = getColor("yellow",xintensity)
            orange = getColor("orange",xintensity)
            white = getColor("white",xintensity)
            if event.code == 310 and event.value == 1:
                print("trigger")
                menuWipe(orange)
                menu_data = 0
                show4bit(menu_data,orange,green)
            if event.code == 316 and event.value == 1:
                print("start")
                in_menu = False
                escaping_menu = True
                xintensity = previous_intensity
                color = previous_color
                doChase((xintensity*color[0],xintensity*color[1],xintensity*color[2]), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 305 and event.value == 1:
                print("a")
            if event.code == 306 and event.value == 1:
                print("b")
            if event.code == 308 and event.value == 1:
                print("left shoulder")
            if event.code == 309 and event.value == 1:
                print("right shoulder")
            if event.code == 313 and event.value == 1:
                print("north")
            if event.code == 312 and event.value == 1:
                print("east")
            if event.code == 304 and event.value == 1:
                print("south")
            if event.code == 307 and event.value == 1:
                print("west")
            if event.code == 17 and event.value == -1:
                print("dpad up")
                if menu_data < 15:
                    menu_data = menu_data + 1
                show4bit(menu_data,orange,green)
            if event.code == 16 and event.value == 1:
                print("dpad right")
            if event.code == 17 and event.value == 1:
                print("dpad down")
                if menu_data > 0:
                    menu_data = menu_data - 1
                show4bit(menu_data,orange,green)
            if event.code == 16 and event.value == -1:
                print("dpad left")
        if in_menu == False:
            if event.code == 310 and event.value == 1:
                print("trigger")
                if xintensity == 255:
                    color = [1,1,1]
                xintensity = 255
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 316 and event.value == 1:
                print("start")
                if escaping_menu == False:
                    previous_intensity = xintensity
                    previous_color = color
                    in_menu = True
                    initWhite(0)
                    orange = (xintensity,int(xintensity*0.5),0)
                    green = (0,xintensity,0)
                    menuWipe(orange)
                    show4bit(0,orange,green)
            if event.code == 305 and event.value == 1:
                print("a")
                if xintensity >= 64:
                    xintensity = xintensity - 32
                if xintensity < 64 and xintensity >= 32:
                    xintensity = xintensity - 16
                if xintensity < 32:
                    xintensity = xintensity - 8
                if xintensity < 0:
                    xintensity = 0
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 306 and event.value == 1:
                print("b")
                if xintensity >= 64:
                    xintensity = xintensity + 32
                if xintensity < 64 and xintensity >= 32:
                    xintensity = xintensity + 16
                if xintensity < 32:
                    xintensity = xintensity + 8
                if xintensity > 255:
                    xintensity = 255
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 308 and event.value == 1:
                print("left shoulder")
                color = [0,0,1]
                doChase((0,0,xintensity), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 309 and event.value == 1:
                print("right shoulder")
                color = [1,0,0]
                doChase((xintensity,0,0), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 313 and event.value == 1:
                print("north")
                color = [0,1,1]
                doChase((0,xintensity,xintensity), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 312 and event.value == 1:
                print("east")
                color = [0,1,0]
                doChase((0,xintensity,0), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 304 and event.value == 1:
                print("south")
                color = [1,0,1]
                doChase((xintensity,0,xintensity), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 307 and event.value == 1:
                print("west")
                color = [1,1,0]
                doChase((xintensity,int(xintensity*0.25),0), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],int((xintensity*0.25))*color[1],xintensity*color[2])
            
            #if event.type == ecodes.EV_ABS:
                #print(event)
            if event.code == 17 and event.value == -1:
                print("dpad up")
                color = [1,1,1]
                doChase((xintensity,xintensity,xintensity), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 16 and event.value == 1:
                print("dpad right")
                os.system("cd /home/pi/Code && git pull https://blurrydude:SecurePass1!@github.com/blurrydude/Code.git")
                doChase((0,xintensity,0), 256, 2, 0, led_count-1)
                os.system("sudo python3 /home/pi/Code/Python/lights.py -n "+str(led_count)+" -m controller")
                exit()
            if event.code == 17 and event.value == 1:
                print("dpad down")
                doTwinkle(xintensity)
                doChase((xintensity*color[0],xintensity*color[1],xintensity*color[2]), 256, 1, 0, led_count-1)
                initColor(xintensity*color[0],xintensity*color[1],xintensity*color[2])
            if event.code == 16 and event.value == -1:
                print("dpad left")
                xintensity = 0
                initWhite(xintensity)
            escaping_menu = False
        config = open("lights.conf","w")
        config.write(str(color[0])+"|"+str(color[1])+"|"+str(color[2])+"|"+str(xintensity))
        config.close()

def getColor(name,inten):
    if name == "red":
        return (inten,0,0)
    if name == "green":
        return (0,inten,0)
    if name == "blue":
        return (0,0,inten)
    if name == "cyan":
        return (inten,0,inten)
    if name == "magenta":
        return (inten,0,inten)
    if name == "yellow":
        return (inten,inten,0)
    if name == "orange":
        return (inten,int(inten*0.25),0)
    if name == "white":
        return (inten,inten,inten)
    if name == "random":
        i = int(intensity/16)
        if i < 1:
            i = 1
        r = random.randint(1,16)*i
        g = random.randint(1,16)*i
        b = random.randint(1,16)*i
        return (r,g,b)
def show4bit(b,ca,cb):
    pixels[0] = ca if b & 1 else cb
    pixels[2] = ca if b & 2 else cb
    pixels[4] = ca if b & 4 else cb
    pixels[6] = ca if b & 8 else cb

def menuWipe(c):
    pixels[0] = c
    time.sleep(0.1)
    pixels[1] = c
    time.sleep(0.1)
    pixels[2] = c
    pixels[0] = (0,0,0)
    time.sleep(0.1)
    pixels[3] = c
    pixels[1] = (0,0,0)
    time.sleep(0.1)
    pixels[4] = c
    pixels[2] = (0,0,0)
    time.sleep(0.1)
    pixels[5] = c
    pixels[3] = (0,0,0)
    time.sleep(0.1)
    pixels[6] = c
    pixels[4] = (0,0,0)
    time.sleep(0.1)
    pixels[7] = c
    pixels[5] = (0,0,0)
    time.sleep(0.1)
    pixels[6] = (0,0,0)
    time.sleep(0.1)
    pixels[7] = (0,0,0)

def menuWipeReverse(c):
    pixels[7] = c
    time.sleep(0.1)
    pixels[6] = c
    time.sleep(0.1)
    pixels[5] = c
    pixels[7] = (0,0,0)
    time.sleep(0.1)
    pixels[4] = c
    pixels[6] = (0,0,0)
    time.sleep(0.1)
    pixels[3] = c
    pixels[5] = (0,0,0)
    time.sleep(0.1)
    pixels[2] = c
    pixels[4] = (0,0,0)
    time.sleep(0.1)
    pixels[1] = c
    pixels[3] = (0,0,0)
    time.sleep(0.1)
    pixels[0] = c
    pixels[2] = (0,0,0)
    time.sleep(0.1)
    pixels[1] = (0,0,0)
    time.sleep(0.1)
    pixels[0] = (0,0,0)

initWhite(0)
time.sleep(0.5)
color = selectColor(colorWord, intensity)
if mode == "chase":
    doChase(color, speed, loops, start, end)
    initWhite(endstate)
if mode == "static":
    doOn(color,0,led_count)
if mode == "range":
    doOn(color,0,led_count)
if mode == "ui":
    doUI()
if mode == "controller":
    doController()