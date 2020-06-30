from sklearn import svm
from pymongo import MongoClient
import numpy as np
import pprint
import matplotlib.pyplot as plt

# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29
user = db.essai
#stock de donnees (X : points, Y : labels)
X= []
y = []
for info in user.find({"label_agr_visi": {"$exists":"true"}},{"agressivity":1, "_id":1, "visibilite_moy":1, "label_agr_visi":1}):
    x=[[info.get("PC1"), info.get("PC2")]]
    X=X+x
    y.append(info.get("label_agr_visi"))
#On converti X en np array pour mieux l'utiliser apres
X=np.array(X)
y=np.array(y)
#definition du calassifier
clf = svm.SVC(kernel='linear')
clf.fit(X,y)
#on defini le separateur
w = clf.coef_[0]
a = -w[0] / w[1]

xx = np.linspace(0,12)
yy = a * xx - clf.intercept_[0] / w[1]

#separateur
h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

# points avec differentes couleurs
plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()
