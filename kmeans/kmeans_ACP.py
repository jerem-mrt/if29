from pymongo import MongoClient
import numpy as np
from pprint import pprint
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29
users = db.user.find()
i=0

#faire un tableau avec PC1 et PC2 et id user
tableau=[]
for x in users :
    tableau.append([x.get("PC1"),x.get("PC2")])

    
print('tableau rempli')

# Create a KMeans model with n clusters: kmeans
model = KMeans(n_clusters=5)

### Fit pipeline to the daily price movements
model.fit(tableau)

#associe les labels aux points
labels = model.predict(tableau)

print(model.inertia_)
#créer et affiche le graphe
xs = []
ys = []
for x in tableau:
    xs.append(x[0])
    ys.append(x[1])
    
plt.scatter(xs,ys,c=labels, alpha=0.5)
plt.show()
