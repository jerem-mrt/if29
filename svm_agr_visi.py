from sklearn import svm
from pymongo import MongoClient
import numpy as np
from pprint import pprint
# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29
user = db.user
X= []
y = []
for info in user.find({"label_agr_visi": {"$exists":"true"}},{"agressivity":1, "_id":1, "visibilite_moy":1, "label_agr_visi":1}).limit(5000):
    x=[[info.get("agressivity"), info.get("visibilite_moy")]]
    X=X+x
    y.append(info.get("label_agr_visi"))
    
clf = svm.SVC()
clf.fit(X[0:1000],y[0:1000])
toPredictArray = X[1001:4000]
clf.predict(toPredictArray)
