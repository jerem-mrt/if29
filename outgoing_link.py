# -*- coding: cp1252 -*-
import pymongo

#lien avec MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/");
db = client['if29'];

#lien avec collection tweet
tweet = db["tweet"];

#lien avec collection user
user = db["user"];

#initalisation des variables
stock={};
for x in tweet.find():
    utilisateur=x.get("user").get("id")
    #Nombre de liens externes
    outgoing_link=x.get("entities").get("urls")
    outgoing_link = len(outgoing_link)
    if not user.find_one({"_id": utilisateur}):
        db.user.insert_one({"_id" : utilisateur, "outgoing_link" : outgoing_link})
    else :
        db.user.update_one({"_id" : utilisateur},{"$set":{ "outgoing_link" : outgoing_link}})
 
    

    
