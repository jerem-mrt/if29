from pymongo import MongoClient
import numpy as np
from pprint import pprint

#lien avec mongoDB
client = MongoClient('localhost', 27017)
db = client.if29
tweet = db.tweet

#on récupère l'ensemble des tweets
tweets = db.tweet.find()

#lien avec la collection user
user = db.user
      

pipeline = [
	{"$group" : {"_id" : "$user.id", "nb_caractere" : {"$avg" : {"$strLenCP" : "$text"}}}}
]
longueurs = list(db.tweet.aggregate(pipeline))
#on enregistre le résultat dans mongodb
for longueur in longueurs:
	if not db.user.find_one({"_id": longueur}):
                db.user.insert_one({"_id" : longueur,"nb_caractere" : longueurs[longueur]["nb_caractere"]})
	else:
                db.user.update_one({"_id" : longueur},{"$set" : {"nb_caractere" : longueurs[longueur]["nb_caractere"]}})



# #longueurs stocke les données qui nous intéresse
# longueurs = {}

# # On execute la requête et pour chacun des tweets, on conserve les données qui nous intéressent
# for tweet in tweets:
#     # Si l'utilisateur n'a pas encore été rencontré, on l'ajoute à notre dictionnaire longueur
#     if tweet['user']['id'] not in longueurs:
#         longueurs[tweet['user']['id']] = {}
#         longueurs[tweet['user']['id']]['longueur_tweet'] = []
#         longueurs[tweet['user']['id']]['longueur_tweet'].append(len(tweet['text']))
        
#     # Sinon on ajoute l'id d'utilisateur au dictionnaire longueur
#     else :
#         longueurs[tweet['user']['id']]['longueur_tweet'].append(len(tweet['text']))

# for longueur in longueurs:
# 	longueurs[longueur]['longueur_tweet'].sort(reverse=True)
# 	# S'il y a plus d'un tweet de retenu, on additionne on additionne le nombre de caractères et on divise par le nombre de tweet
# 	n = longueurs[longueur]['longueur_tweet']
# 	if n>1:
# 		longueurs[longueur]['longueur_moy'] = 

# rajouter dans la collection user

# db.getCollection("Tweets").aggregate(
#    [
#      {    $group : {
#         "_id" : "$user.id",
#         "nb_caractere" : { $avg: {  $strLenCP: "$text"  }}
#         }
#     },
#     {    $sort : {
#         "nb_caractere" : 1
#         }
#     }
#    ]
# )
