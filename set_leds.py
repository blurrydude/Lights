import copy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/ian/hydroponic_control/fsa.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def getRef(path):
    path = path.split('/')
    if len(path) == 2:
        ref = db.collection(path[0]).document(path[1])
    else:
        ref = db.collection(path[0])
    return ref

config_ref = getRef('LightConfig/clockpi')
config = config_ref.get().to_dict()

def get_palette():
    r = 16
    g = 0
    b = 0
    p = []
    for i in range(48):
        if g < 16 and b == 0:
            r = r - 1
            g = g + 1
        elif b < 16 and r == 0:
            g = g - 1
            b = b + 1
        else:
            b = b - 1
            r = r + 1
        p.append({"r":r,"g":g,"b":b})
    last = copy.copy(p[len(p)-1])
    del p[len(p)-1]
    p.insert(0,last)
    return p

def pattern_1():
    global config
    step = 1
    tr = step * 30
    tg = 0
    tb = 0
    for i in range(len(config["pixels"])):
        config["pixels"][i]["r"] = tr
        config["pixels"][i]["g"] = tg
        config["pixels"][i]["b"] = tb
        if tr > 0:
            tr = tr - step
            tg = tg + step
        if tr == 0:
            tg = tg - step
            tb = tb + step

def pattern_2():
    global config
    config["pixels"][8] = {"r":0,"g":0,"b":0}
    config["pixels"][9] = {"r":0,"g":0,"b":0}
    config["pixels"][10] = {"r":0,"g":0,"b":0}
    config["pixels"][11] = {"r":0,"g":0,"b":0}
    palette = get_palette()
    for i in range(len(palette)):
        config["pixels"][i+12] = palette[i]

pattern_2()
config_ref.set(config)