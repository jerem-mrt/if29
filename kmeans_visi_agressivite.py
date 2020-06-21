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

#faire un tableau avec visibilite et agressivite et id user
tableau=[]
for x in users :
    tableau.append([x['visibilite_moy'],x['agressivity']])

    
print('tableau rempli')

### Create a normalizer: normalizer
normalizer = Normalizer()

# Create a KMeans model with 10 clusters: kmeans
model = KMeans(n_clusters=2)

### Make a pipeline chaining normalizer and kmeans: pipeline
pipeline = make_pipeline(normalizer,model)


### Fit pipeline to the daily price movements
pipeline.fit(tableau)

##kmeans = model.fit(tableau)
labels = pipeline.predict(tableau)

print(model.inertia_)

xs = []
ys = []
for x in tableau:
    xs.append(x[0])
    ys.append(x[1])
    
plt.scatter(xs,ys,c=labels, alpha=0.5)
plt.show()
