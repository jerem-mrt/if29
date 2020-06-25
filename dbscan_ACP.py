import numpy as np 
import pymongo 
 
from sklearn.cluster import DBSCAN 
from sklearn.preprocessing import scale 
 
 
# ############################################################################# 
#Lien avec la collection user 
client = pymongo.MongoClient("mongodb://localhost:27017/"); 
db = client['if29']; 
user = db["user"]; 
X=[] 
utilisateurs=[] 
for info in user.find({"agressivity":{"$gt":0}, "visibilite_moy":{"$gt":0}},{"agressivity":1, "_id":1, "visibilite_moy":1}).limit(5000): 
    x=[[info.get("agressivity"), info.get("visibilite_moy")]] 
    X=X+x 
    #we want to keep the id of the user to put the labels back in mongoDB for a supervised algorithm 
    utilisateur=[info.get("_id")] 
    utilisateurs=utilisateurs+utilisateur 
     
X=np.array(X) 
# ############################################################################# 
# Compute DBSCAN 
db = DBSCAN(eps=0.1, min_samples=5).fit(X)              
#Definition of the core points 
core_samples_mask = np.zeros_like(db.labels_, dtype=bool) 
core_samples_mask[db.core_sample_indices_] = True 
#label of the clusters 
labels = db.labels_ 
for ind in range(len(labels)) : 
    utilisateur=int(utilisateurs[ind]) 
    user.update_one({"_id": utilisateur},{"$set" :{"label_agr_visi" : int(labels[ind])}}) 
 
# Number of clusters in labels, ignoring noise if present. 
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  
n_noise_ = list(labels).count(-1) 
 
print('Estimated number of clusters: %d' % n_clusters_) 
print('Estimated number of noise points: %d' % n_noise_) 
 
# ############################################################################# 
# Plot result 
import matplotlib.pyplot as plt 
 
# Black removed and is used for noise instead. 
unique_labels = set(labels) 
#setting the colors of the clusters 
colors = [plt.cm.Spectral(each) 
          for each in np.linspace(0, 1, len(unique_labels))] 
for k, col in zip(unique_labels, colors): 
    if k == -1: 
        # Black used for noise. 
        col = [0, 0, 0, 1] 
         
    class_member_mask = (labels == k) 
 
    xy = X[class_member_mask & core_samples_mask] 
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), 
             markeredgecolor='k') 
 
#plotting graph 
plt.title('Estimated number of clusters: %d' % n_clusters_) 
plt.show() 
