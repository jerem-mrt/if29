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
for x in tweet.find({},{"user.followers_count":1, "user.friends_count":1, "user.id":1, "_id":0}):
    utilisateur=x.get("user").get("id")
    #Nombre de compte suivis 
    nbComptesSuivis=x.get("user").get("followers_count");
    #Nombre de followers
    nbFollowers=x.get("user").get("friends_count");
    #ratio
    if (nbFollowers != 0) : 
        ratio=float(nbComptesSuivis)/float(nbFollowers);
    else :
        ratio=0
    #ajoute dans user
    if not user.find_one({"_id": utilisateur}):
        db.user.insert_one({"_id" : utilisateur, "nbFollowers" : nbFollowers, "nbComptesSuivis" : nbComptesSuivis, "ratio" : ratio})
    else :
        db.user.update_one({"_id" : utilisateur},{"$set":{ "nbFollowers" : nbFollowers, "nbComptesSuivis" : nbComptesSuivis, "ratio" : ratio}})
 
    

    
