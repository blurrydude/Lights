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

config_ref = getRef('LightConfig/canvaspi')
config = config_ref.get().to_dict()
# tr = 5
# tb = 245
# for i in range(len(config["pixels"])):
#     config["pixels"][i]["b"] = tb
#     config["pixels"][i]["g"] = 0
#     config["pixels"][i]["r"] = tr
#     tb = tb - 5
#     tr = tr + 5
for i in range(len(config["pixels"])):
    config["pixels"][i]["b"] = 0
    config["pixels"][i]["g"] = 127
    config["pixels"][i]["r"] = 0
config_ref.set(config)