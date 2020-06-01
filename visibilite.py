import pymongo
from pymongo import MongoClient
import pprint
import datetime
import numpy as np

#lien avec mongoDB
client = MongoClient('localhost', 27017)
db = client.if29
collection = db.tweet
i=0
taille_moy_mention = 11.4
float(taille_moy_mention)
taille_moy_tag = 11.6
float(taille_moy_tag)

#récupération nombre de # et de mention 
for x in collection.find({},{"entities.hashtags":1,"entities.user_mentions":1, "_id":0}):
    print("Tweet numero %d"%(i))
    i+=1
    print("Nombre de hashtags : ")
    tag_tweet = len(x.get("entities").get("hashtags"))
    float(tag_tweet)
    print(tag_tweet)
    print("Nombre de mentions : ")
    mention_tweet = len(x.get("entities").get("user_mentions"))
    float(mention_tweet)
    print(mention_tweet)
    #calcul de la visibilité
    print("Visibilité du tweet : ")
    visibilite = (mention_tweet * taille_moy_mention + tag_tweet * taille_moy_tag)/140
    print(visibilite)


