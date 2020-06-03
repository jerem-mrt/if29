import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/");
mydb = myclient['projet'];
mycol = mydb["tweet"];

for x in mycol.find({},):
	#pour chaque profil, compte le nombre de caractères moyens dans les tweets et en fait la moyenne