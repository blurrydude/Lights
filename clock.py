import requests
from datetime import datetime
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 60)

def setPixel(p,r,g,b):
    #requests.get('http://192.168.1.236/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(p)+'&z='+str(p))
    pixels[p] = (r,g,b)

def setRange(a,z,r,g,b):
    #requests.get('http://192.168.1.236/?r='+str(r)+'&g='+str(g)+'&b='+str(b)+'&a='+str(a)+'&z='+str(z))
    while a <= z:
        setPixel(a,r,g,b)
        a = a + 1

# doSeconds = False

# now = datetime.now()
# hour = now.hour
# postmeridian = hour > 11
# hourColor = (0,255,0)
# minuteColor = (0,0,255)
# if postmeridian == True:
#     hour = hour - 12
#     hourColor = (255,0,0)
# hourhand = hour * 5
# if hourhand == 60:
#     hourhand = 0
# minutehand = now.minute
# second = now.second
# tick = 0
# #setRange(0,59,0,0,0)
# if minutehand == hourhand:
#     if postmeridian == True:
#         setPixel(hourhand,255,0,255)
#     else:
#         setPixel(hourhand,0,255,255)
# else:
#     if postmeridian == True:
#         setPixel(hourhand,255,0,0)
#     else:
#         setPixel(hourhand,0,255,0)
#     setPixel(minutehand,0,0,255)
# # if hourhand == 0:
# #     setPixel(55,0,0,0)
# # if hourhand > 0:
# #     setPixel(hourhand-5,0,0,0)
# if minutehand == 0:
#     setPixel(59,0,0,0)
# if minutehand > 0:
#     setPixel(minutehand-1,0,0,0)
# for i in range(12):
#     m = i * 5
#     if m != hourhand and m != minutehand:
#         setPixel(m,32,4,0)

# if second > 0:
#     for x in range(second+2):
#         if x != minutehand and x != hourhand:
#             if x % 5 == 0:
#                 setPixel(x,0,4,32)
#             else:
#                 setPixel(x,8,0,16)
# lastsecond = 0
# while datetime.now().minute == minutehand:
#     if datetime.now().second != lastsecond:
#         lastsecond = datetime.now().second
#         if lastsecond != minutehand and lastsecond != hourhand:
#             if lastsecond % 5 == 0:
#                 setPixel(lastsecond,0,4,32)
#             else:
#                 setPixel(lastsecond,8,0,16)

# # nexttick = 0
# # if doSeconds == True:
# #     while datetime.now().minute == minutehand or datetime.now().second < startsecond -2:
# #         if tick == nexttick:
# #             if minutehand != tick and hourhand != tick:
# #                 if tick == 0:
# #                     setPixel(0,0,4,32)
# #                 elif tick == 5:
# #                     setPixel(5,0,4,32)
# #                 elif tick == 10:
# #                     setPixel(10,0,4,32)
# #                 elif tick == 15:
# #                     setPixel(15,0,4,32)
# #                 elif tick == 20:
# #                     setPixel(20,0,4,32)
# #                 elif tick == 25:
# #                     setPixel(25,0,4,32)
# #                 elif tick == 30:
# #                     setPixel(30,0,4,32)
# #                 elif tick == 35:
# #                     setPixel(35,0,4,32)
# #                 elif tick == 40:
# #                     setPixel(40,0,4,32)
# #                 elif tick == 45:
# #                     setPixel(45,0,4,32)
# #                 elif tick == 50:
# #                     setPixel(50,0,4,32)
# #                 elif tick == 55:
# #                     setPixel(55,0,4,32)
# #             # else:
# #             #     setPixel(tick,8,0,16)
# #             nexttick = tick + 1
# #         if second != datetime.now().second:
# #             second = datetime.now().second
# #             tick = tick + 1
second = -1
minute = -1
hour = -1
background = []
setRange(0,59,0,0,0)
for i in range(60):
    if i != 0 and i % 15 == 0:
        background.append((32,4,0))
    elif i % 5 == 0:
        background.append((8,1,0))
    else:
        background.append((0,0,0))
for i in range(12):
    setPixel(i*5,32,4,0)
    background[i*5] = (32,4,0)
while True:
    now = datetime.now()
    hour = now.hour
    pm = hour > 11
    dhour = hour
    if pm == True:
        dhour = dhour - 12
    hand = dhour * 5
    if now.second != second:
        second = now.second
        if second != now.minute and second != hand:
            setPixel(second,0,255,0)
        if second == now.minute and second != hand:
            setPixel(second,0,255,255)
        if second != now.minute and second == hand:
            setPixel(second,255,255,0)
        if second == now.minute and second == hand:
            setPixel(second,255,255,255)
        if second == 0:
            l = background[59]
            if now.minute == 59:
                setPixel(59,0,0,255)
            else:
                setPixel(59,l[0],l[1],l[2])
        else:
            l = background[second-1]
            if now.minute == second-1 and hand == second-1:
                setPixel(second-1,255,0,255)
            if now.minute != second-1 and hand == second-1:
                setPixel(second-1,255,0,0)
            if now.minute == second-1 and hand != second-1:
                setPixel(second-1,0,0,255)
            if now.minute != second-1 and hand != second-1:
                setPixel(second-1,l[0],l[1],l[2])
    if now.minute != minute:
        minute = now.minute
        if minute != second:
            if minute != hand:
                setPixel(minute,0,0,255)
            if minute == hand:
                setPixel(minute,255,0,255)
            if minute == 0:
                if second != 59:
                    l = background[59]
                    setPixel(59,l[0],l[1],l[2])
            else:
                if minute-1 != hand and minute-1 != second:
                    l = background[minute-1]
                    setPixel(minute-1,l[0],l[1],l[2])
                if minute-1 == hand and minute-1 != second:
                    setPixel(minute,255,0,0)
    if now.hour != hour:
        if hand != minute and hand != second:
            if hand != minute and hand != second:
                print('setting hour '+str(hand))
                setPixel(hand,255,0,0)
            if hand == 0:
                if minute != 59 and second != 59:
                    l = background[59]
                    setPixel(59,l[0],l[1],l[2])
            else:
                if minute != hand-1 and second != hand-1:
                    l = background[hand-1]
                    setPixel(hand-1,l[0],l[1],l[2])


