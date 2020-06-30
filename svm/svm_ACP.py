from sklearn import svm
from pymongo import MongoClient
import numpy as np
import pprint
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29
user = db.user
#stock de donnees (X : points, Y : labels)
X= []
y = []
aPredire = []
for info in user.find({"suspect" : {"$exists" : True}}, {"PC1":1,"PC2":1, "suspect":1}):
    x=[[info.get("PC1"), info.get("PC2"), info.get("_id")]]
    X=X+x
    y.append(info.get("suspect"))

print("Récupération des données labelisées effectuée")

# On récolte les utilisateurs à prédire
for info in user.find({"suspect" : {"$exists" : False}}, {"PC1":1,"PC2":1}):
    aPredire.append([info.get("PC1"), info.get("PC2"), info.get("_id")])
print("Récupération données effectuée")
#On converti X en np array pour mieux l'utiliser après
X=np.array(X)
y=np.array(y)
aPredire = np.array(aPredire)
print("Array effectuées")
#definition du classifier
clf = svm.SVC(kernel='poly')
clf.fit(X[:,(0,1)],y)
print("Fit effectué")
prediction= clf.predict(aPredire[:, (0,1)])
yVisualisation = np.append(y, prediction)
XVisualisation = np.append(X[:, (0,1)], aPredire[:, (0,1)], axis=0)

print("Définition des coefficients")

#points avec différentes couleurs
plt.scatter(XVisualisation[:, 0], XVisualisation[:, 1], c = yVisualisation )
plt.legend()
plt.show()
n=0
for utilisateur in range(len(aPredire)) :
    id = aPredire[utilisateur][2]
    if not user.find_one({"_id": id}):
        #print("L'utilisateur " + str(id) + " n'a pas été trouvé")
        n=n+1
    else :
        db.user.update_one({"_id" : id},{"$set": {"label_svm" : int(prediction[utilisateur])}})

