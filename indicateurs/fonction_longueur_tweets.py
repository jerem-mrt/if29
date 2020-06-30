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
longueurs = list(tweet.aggregate(pipeline,allowDiskUse=True))

#on enregistre le résultat dans mongodb
for longueur in longueurs:
	if not db.user.find_one({"_id": longueur['_id']}):
		db.user.insert_one({"_id" : longueur['_id'],"nb_caractere" : longueur["nb_caractere"]})
	else:
		db.user.update_one({"_id" : longueur['_id']},{"$set" : {"nb_caractere" : longueur["nb_caractere"]}})



