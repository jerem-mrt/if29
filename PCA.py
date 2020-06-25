import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Lien avec MongoDB
client = pymongo.MongoClient("localhost", 27017)

db = client.if29
users = db.user
tabUser = []
idTag = []

# Récupération des variables analysées dans le tableau 'user'
for x in users.find():
    tabUser.append([x['visibilite_moy'], x['agressivity'], x['frequenceTweet'], x['nbFollowers'], x['outgoing_link'], x['mention_tweet'], x['nbComptesSuivis'], x['tag_tweet']])
    idTag.append([x['_id']])

##df = pd.DataFrame(data=tabUser)
##dfId = pd.DataFrame(data=idTag)
##df.columns = ['visibilite_moy', 'agressivity', 'frequenceTweet', 'nbFollower', 'outgoing_link', 'mention_tweet', 'nbComptesSuivis', 'tag_tweet']

#Séparations des colonnes
features = ['visibilite_moy', 'agressivity', 'frequenceTweet', 'nbFollower', 'outgoing_link', 'mention_tweet', 'nbComptesSuivis', 'tag_tweet']
##
x = tabUser#.loc[:, features].values
x = StandardScaler().fit_transform(x)

# Application de la PCA pour réduire à un tabUser 2-dim
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
##principalDf = pd.DataFrame(data=principalComponents, columns=['principalComponent1', 'principalComponent2'])

# Juxtaposition de l'id avant insertion dans la table user
##principalDf[['id']] = idTag
##cols = principalDf.columns.tolist()
##cols = cols[-1:] + cols[:-1]
##principalDf = principalDf[cols]

##principalDf=[]
##for y in range(len(idTag)):
##    principalDf.append([idTag[y],principalComponents[y][0],principalComponents[y][1]])
##
print(principalComponents)

##
##pctempo = []

# Update de la base user
for uti in range(len(principalComponents)):
##    pc1 = principalDf['principalComponent1'][principalDf['id']== uti].values[0]
##    pc1 = float(pc1)
##    pc2 = principalDf['principalComponent2'][principalDf['id']== uti].values[0]
##    pc2 = float(pc2)
##    pctempo.append([uti, pc1, pc2])  
    #db.user.update_one({"_id": int(uti)}, {"$set": {"PC1": pc1, "PC2": pc2}})
    if not users.find_one({"_id": idTag[uti][0]}):
        db.users.insert_one({"_id": idTag[uti][0],"PC1": principalComponents[uti][0], "PC2": principalComponents[uti][1]})
    else :
        db.users.update_one({"_id": idTag[uti][0]}, {"$set": {"PC1": principalComponents[uti][0], "PC2": principalComponents[uti][1]}})


#Affichage

xs = []
ys = []
for z in principalComponents:
    xs.append(z[0])
    ys.append(z[1])
    


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=10)
ax.set_ylabel('Principal Component 2', fontsize=10)
ax.set_title('2 component PCA', fontsize=20)

plt.scatter(xs,ys, s=1)
plt.show()
##columns = principalDf.columns
##
##x = principalDf[['principal component 1']]
##y = principalDf[['principal component 2']]
##
##plt.scatter(x, y, s=1)
##
##plt.show()

