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
taille_moy_mention = 11.4
float(taille_moy_mention)
taille_moy_tag = 11.6
float(taille_moy_tag)
last_user=0
moyenne_visibilite=0
i=0
##
##pipeline=[{"$sort" : {"user.id" : 1}}]
##liste = list(db.tweet.aggregate(pipeline,allowDiskUse=True))
#On récupère l'ensempble des tweet
tweets = db.tweet.find()

#On va stocker les données dont on a besoin dans stock
stock ={}
nb_tweet = 0
#récupération nombre de # et de mention par tweet et stockage dans stock
for x in tweets : 
    #récupération de l'id de l'utilisateur
    user_id = x.get("user").get("id")
    tag_tweet = len(x.get("entities").get("hashtags"))
    float(tag_tweet)
    mention_tweet = len(x.get("entities").get("user_mentions"))
    float(mention_tweet)
    if user_id not in stock :
        nb_tweet = 1
        stock[x['user']['id']]={}
        stock[x['user']['id']]['tag_tweet']=tag_tweet
        stock[x['user']['id']]['mention_tweet']=mention_tweet
        stock[x['user']['id']]['nb_tweet']=nb_tweet
    else :
        stock[x['user']['id']]['nb_tweet']=stock[x['user']['id']]['nb_tweet'] +1
        stock[x['user']['id']]['tag_tweet']= stock[x['user']['id']]['tag_tweet'] + tag_tweet
        stock[x['user']['id']]['mention_tweet'] = stock[x['user']['id']]['mention_tweet'] + mention_tweet

print("stock rempli")

# On détermine la visibilité de chacun des profiles
for y in stock:
    # S'il y a plus d'un tweet de retenu, on additionne la visibilité et on divise par le nombre de tweet
    n = stock[y]['nb_tweet']
    if n>1:
        stock[y]['visibilite_moy'] = (((stock[y]['tag_tweet']*taille_moy_mention)+(stock[y]['tag_tweet'] * taille_moy_tag))/140)/stock[y]['nb_tweet']
        
    else :
        stock[y]['visibilite_moy'] = (stock[y]['mention_tweet'] * taille_moy_mention + stock[y]['tag_tweet'] * taille_moy_tag)/140

# On enregistre les résultats dans MongoDB
for y in stock :
    if not user.find_one({"_id": y}):
        print(utilisateur)
        db.user.insert_one({"_id" : y, "tag_tweet" : stock[y]['tag_tweet'], "mention_tweet" : stock[y]['mention_tweet'], "visibilite_moy" : stock[y]['visibilite_moy']})
    else :
        db.user.update_one({"_id" : y},{"$set": {"tag_tweet" : stock[y]['tag_tweet'], "mention_tweet" : stock[y]['mention_tweet'], "visibilite_moy" : stock[y]['visibilite_moy']}})
 
