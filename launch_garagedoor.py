import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-ip", help="ip address")
parser.add_argument("--s", "-s", help="whether or not to use sensor input (0 or 1)")
args = parser.parse_args()

os.system('sudo python3 /home/pi/Lights/garagedoor.py -ip '+args.ip+' -s '+args.s)