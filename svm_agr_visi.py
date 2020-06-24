from sklearn import svm
from pymongo import MongoClient
import numpy as np
import pprint
import matplotlib.pyplot as plt

# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29
user = db.user
#stock de donnees (X : points, Y : labels)
X= []
y = []
for info in user.find({"label_agr_visi": {"$exists":"true"}},{"agressivity":1, "_id":1, "visibilite_moy":1, "label_agr_visi":1}).limit(5000):
    x=[[info.get("agressivity"), info.get("visibilite_moy")]]
    X=X+x
    y.append(info.get("label_agr_visi"))
#On converti X en np array pour mieux l'utiliser après
X=np.array(X)
y=np.array(y)
#definition du calassifier
clf = svm.SVC(kernel='linear')
clf.fit(X[0:1000],y[0:1000])
#on defini le separateur
w = clf.coef_[0]
a = -w[0] / w[1]

xx = np.linspace(0,12)
yy = a * xx - clf.intercept_[0] / w[1]

#séparateur
h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

# points avec différentes couleurs
plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()
