import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Lien avec MongoDB
client = pymongo.MongoClient("localhost", 27017)

db = client.if29
users = db.user.find().limit(10000)
tabUser = []
idTag = []

# Récupération des variables analysées dans le tableau 'user'
for x in users:
    tabUser.append([x['frequenceTweet'], x['nbFollowers'], x['outgoing_link'], x['mention_tweet'], x['nbComptesSuivis'], x['tag_tweet']])
    idTag.append([x['_id']])

df = pd.DataFrame(data=tabUser)
dfId = pd.DataFrame(data=idTag)
df.columns = ['frequenceTweet', 'nbFollower', 'outgoing_link', 'mention_tweet', 'nbComptesSuivis', 'tag_tweet']

# Séparations des colonnes
features = ['frequenceTweet', 'nbFollower', 'outgoing_link', 'mention_tweet', 'nbComptesSuivis', 'tag_tweet']

x = df.loc[:, features].values
x = StandardScaler().fit_transform(x)

# Application de la PCA pour réduire à un tabUser 2-dim
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data=principalComponents, columns=['principalComponent1', 'principalComponent2'])

# Juxtaposition de l'id avant insertion dans la table user
principalDf[['id']] = dfId
cols = principalDf.columns.tolist()
cols = cols[-1:] + cols[:-1]
principalDf = principalDf[cols]

print(principalDf)

# Update de la base user
for uti in principalDf['id'].values:
    pc1 = principalDf['principalComponent1'][principalDf['id']== uti].values[0]
    pc1 = float(pc1)
    pc2 = principalDf['principalComponent2'][principalDf['id']== uti].values[0]
    pc2 = float(pc2)
    db.essai.insert_one({"_id": int(uti),"PC1": pc1, "PC2": pc2})

"""
#Affichage

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=10)
ax.set_ylabel('Principal Component 2', fontsize=10)
ax.set_title('2 component PCA', fontsize=20)

columns = principalDf.columns

x = principalDf[['principal component 1']]
y = principalDf[['principal component 2']]

plt.scatter(x, y, s=1)

plt.show()
"""