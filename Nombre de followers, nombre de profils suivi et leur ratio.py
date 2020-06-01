# -*- coding: cp1252 -*-
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/");
mydb = myclient['projet'];
mycol = mydb["tweet"];
i=0;
for x in mycol.find({},{"user.followers_count":1, "user.friends_count":1, "_id":0}):
    print"Tweet numero %d"%(i);
    i+=1
    print("Nombre de compte suivis : ")
    print(x.get("user").get("followers_count"));
    print("Nombre de followers : ")
    print(x.get("user").get("friends_count"));
    print("Ratio :");
    if (x.get("user").get("friends_count")!=0):
        print(x.get("user").get("followers_count")/x.get("user").get("friends_count"));
    else :
        print("division par 0")
