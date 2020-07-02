import numpy as np
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import pymongo


# #############################################################################
#Lien avec la collection user
client = pymongo.MongoClient("mongodb://localhost:27017/");
db = client['if29'];
user = db["user"];

# #############################################################################
#Creation de X
X=[]
for info in user.find({},{"PC1":1, "_id":0, "PC2":1}):
    X.append([info["PC1"], info["PC2"]])

neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(X)
distances, indices = nbrs.kneighbors(X)
distances = np.sort(distances, axis=0)
distances_i = distances[:,1]
y=range(len(distances_i))
print(distances_i)
plt.plot(distances_i)
plt.show()
