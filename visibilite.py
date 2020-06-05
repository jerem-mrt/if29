import pymongo
from pymongo import MongoClient
import pprint
import datetime
import numpy as np

#lien avec mongoDB
client = MongoClient('localhost', 27017)
db = client.if29
tweet = db.tweet

#lien avec la collection user
user = db.user

i=0
n=0
taille_moy_mention = 11.4
float(taille_moy_mention)
taille_moy_tag = 11.6
float(taille_moy_tag)
user_id_meme=5549
n=0
moyenne_visibilite=0


#récupération nombre de # et de mention 
for x in tweet.find({},{"entities.hashtags":1,"entities.user_mentions":1, "_id":0, "user.id":1}).sort("user.id",1):
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
    #récupération de l'id de l'utilisateur
    user_id = x.get("user").get("id")
    print(user_id)
    if user_id==user_id_meme:
        n=n+1
        user_id_meme = user_id
        moyenne_vibilite = (visibilite + moyenne_visibilite)/n
        user.insert_many({'id':user_id , "visibilite":moyenne_vibilite})
        print('done')
    else:
        print('user suivant')
