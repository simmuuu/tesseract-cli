import json
import os

db = os.path.join("db", "db.json")

def loadDB():
    if os.path.exists(db):
        with open(db, "r") as d:
            return json.load(d)
    else: 
        return {}

def saveDB(data):
    with open(db, "w") as d:
        json.dump(data, d, indent=4)

def setDB(data):
    saveDB(data)

def getDB(key):
    data = loadDB() 
    return data.get(key, None) 
