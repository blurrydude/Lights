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


config_ref.set(config)