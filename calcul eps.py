import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
import pymongo
import seaborn as sns
sns.set()

# #############################################################################
#Lien avec la collection user
client = pymongo.MongoClient("mongodb://localhost:27017/");
db = client['if29'];
user = db["user"];

# #############################################################################
#Creation de X
X=[]
for info in user.find({},{"agressivity":1, "_id":0, "visibilite_moy":1}):
    x=[[info["agressivity"], info["visibilite_moy"]]]
    X=X+x
X=np.array(X)
print ('fini')

neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(X)
distances, indices = nbrs.kneighbors(X)
distances = np.sort(distances, axis=0)
distances = distances[:,1]
print(distances)
plt.plot(distances)
plt.show()
