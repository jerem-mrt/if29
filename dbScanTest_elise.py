from pymongo import MongoClient
import numpy as np
from pprint import pprint
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# #############################################################################
#Lien avec la collection user
client = MongoClient("localhost",27017)
db=client.if29
user = db["user"]
X=[]
utilisateurs=[]
cursor=user.find({},{"agressivity":1, "_id":1, "visibilite_moy":1},no_cursor_timeout=True).limit(5000)
for info in cursor:
    X.append([info["agressivity"],info["visibilite_moy"]])
    
    #we want to keep the id of the user to put the labels back in mongoDB for a supervised algorithm
    utilisateurs.append(info["_id"])
cursor.close()
# #############################################################################
# Compute DBSCAN
dbScan = DBSCAN(eps=0.5, min_samples=5).fit(X)             

labels=dbScan.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0) 
n_noise_ = list(labels).count(-1)

for ind in range(len(labels)) :
    utilisateur=int(utilisateurs[ind])
    user.update_one({"_id": utilisateur},{"$set" :{"label_agr_visi" : int(labels[ind])}})

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

xs = []
ys = []
for z in X:
    xs.append(z[0])
    ys.append(z[1])
    
plt.scatter(xs,ys,c=labels, alpha=0.5)
plt.show()
