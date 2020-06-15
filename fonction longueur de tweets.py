from pymongo import MongoClient
import numpy as np
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.projet
collection = db["Tweets"]

pipeline = [
	{"$group" : {"_id" : "$user.id", "nb_caractere" : {"$avg" : {"$strLenCP" : "$text"}}}}
]
list(db.collection.aggregate(pipeline))

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