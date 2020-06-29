import pymongo
import json
import pandas as pd
# Lien avec MongoDB
client = pymongo.MongoClient("localhost", 27017)

db = client.if29
essai = db.essai
user = db.user
labels = {}
with open('ids-labelisses.json', 'r') as file:
        labels = json.load(file)

for label in labels :
        labelPropre= label['_id']
        if type(labelPropre)  != int:
                labelPropre = labelPropre['$numberLong']
        
        user.update_one({"_id": labelPropre}, {"$set": {"suspect": label['suspect']}})
print("L'insertion est terminée")
        
