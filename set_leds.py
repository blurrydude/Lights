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

config_ref = getRef('LightConfig/windowpi')
config = config_ref.get().to_dict()

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
    r = 16
    g = 0
    b = 0
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
        config["pixels"][i+9]["r"] = r
        config["pixels"][i+9]["g"] = g
        config["pixels"][i+9]["b"] = b

def pattern_3():
    global config
    r = 8
    g = 0
    b = 0
    for i in range(8,60):
        config["pixels"][i]["r"] = 0
        config["pixels"][i]["g"] = 0
        config["pixels"][i]["b"] = 0
    for i in range(24):
        if g < 8 and b == 0:
            r = r - 1
            g = g + 1
        elif b < 8 and r == 0:
            g = g - 1
            b = b + 1
        else:
            b = b - 1
            r = r + 1
        config["pixels"][i+33]["r"] = r
        config["pixels"][i+33]["g"] = g
        config["pixels"][i+33]["b"] = b

def pattern_4(): # 16 leds
    config["pixels"][0] = { "r":245, "g":245, "b": 66}
    config["pixels"][1] = { "r":245, "g":245, "b": 66}
    config["pixels"][2] = { "r":245, "g":245, "b": 66}
    config["pixels"][3] = { "r": 76, "g":245, "b": 64}
    config["pixels"][4] = { "r": 76, "g":245, "b": 64}
    config["pixels"][5] = { "r": 76, "g":245, "b": 64}
    config["pixels"][6] = { "r": 64, "g":247, "b":220}
    config["pixels"][7] = { "r": 64, "g":247, "b":220}
    config["pixels"][8] = { "r": 64, "g":247, "b":220}
    config["pixels"][9] = { "r": 64, "g":247, "b":220}
    config["pixels"][10] = {"r": 76, "g":245, "b": 64}
    config["pixels"][11] = {"r": 76, "g":245, "b": 64}
    config["pixels"][12] = {"r": 76, "g":245, "b": 64}
    config["pixels"][13] = {"r":245, "g":245, "b": 66}
    config["pixels"][14] = {"r":245, "g":245, "b": 66}
    config["pixels"][15] = {"r":245, "g":245, "b": 66}

pattern_4()
config_ref.set(config)