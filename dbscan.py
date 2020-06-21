import numpy as np
import pymongo

from sklearn.cluster import DBSCAN


# #############################################################################
#Lien avec la collection user
client = pymongo.MongoClient("mongodb://localhost:27017/");
db = client['if29'];
user = db["user"];
X=[]
for info in user.find({},{"agressivity":1, "_id":0, "visibilite_moy":1}):
    x=[[info.get("agressivity"), info.get("visibilite_moy")]]
    X=X+x
X=np.array(X)
# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)             #TODO d�cider de eps
#Definition of the core points
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
#label of the clusters
labels = db.labels_
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


plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()