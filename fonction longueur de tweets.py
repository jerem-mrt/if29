import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/");
mydb = myclient['projet'];
mycol = mydb["Tweets"];

db.getCollection("Tweets").aggregate(
   [
     {    $group : {
        "_id" : "$user.id",
        "nb_caractere" : { $avg: {  $strLenCP: "$text"  }}
        }
    },
    {    $sort : {
        "nb_caractere" : 1
        }
    }
   ]
)