import requests 
import socket

URL = "https://blurrydude.com:5000/checkin"

name = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
d = s.getsockname()
print(d)
ip = d[0]
s.close()

data = '0'

PARAMS = {'name':name, 'ip':ip, 'data':data} 

r = requests.get(url = URL, params = PARAMS)