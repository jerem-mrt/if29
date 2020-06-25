from pymongo import MongoClient
import numpy as np
from pprint import pprint
# Lien avec MongoDB
client = MongoClient("localhost",27017)
db=client.if29

# On se concentre sur la Collection Tweets : on récupère l'ensemble des tweets
tweets = db.tweet.find()
# "Profiles" stockera les données nécessaire au calcul de l'agressivité pour chaque profile
profiles = {}
test= []
# On execute la requête et pour chacun des tweets, on conserve les données qui nous intéressent
for tweet in tweets:
    # Si l'utilisateur n'a pas encore été rencontré, on l'ajoute à notre dictionnaire profiles
    if tweet['user']['id'] not in profiles :
        profiles[tweet['user']['id']] = {}
        profiles[tweet['user']['id']]['timestamp'] = []
        profiles[tweet['user']['id']]['followee'] = []
        profiles[tweet['user']['id']]['followee'].append(int(tweet['user']['friends_count']))
        profiles[tweet['user']['id']]['timestamp'].append(int(tweet['timestamp_ms']))
        
    # Sinon on ajoute l'id d'utilisateur au dictionnaire profiles
    else :
        profiles[tweet['user']['id']]['timestamp'].append(int(tweet['timestamp_ms']))
        profiles[tweet['user']['id']]['followee'].append(int(tweet['user']['friends_count']))
        
print("Parcours des utilisateurs fini")

# On détermine l'agressivité de chacun des profiles
for profile in profiles:
    profiles[profile]['timestamp'].sort(reverse=True)
    timestamp = profiles[profile]['timestamp']
    profiles[profile]['followee'].sort(reverse=True)
    followee = profiles[profile]['followee']
    profiles[profile]['frequenceTweet'] = 1
    profiles[profile]['frequenceFriends'] = 0
    # S'il y a plus d'un tweet de retenu, on additionne les écarts entre chaque tweet
    if len(timestamp) > 1:
        diffTime = timestamp[0] - timestamp[len(timestamp)-1]
        # On convertit le temps en h
        diffTime = diffTime / float(3600000)
        if diffTime > 1 :
            test.append(profile)
            profiles[profile]['frequenceTweet'] = len(timestamp) / diffTime
            diffFriends = (followee[0] - followee[len(followee)-1]) / diffTime
        else :
            profiles[profile]['frequenceTweet'] = len(timestamp)
            diffFriends = (followee[0] - followee[len(followee)-1])
        
    profiles[profile]['agressivity'] = (profiles[profile]['frequenceFriends'] + profiles[profile]['frequenceTweet'])/350
for profile in profiles :
    if not db.user.find_one({"_id": profile}):
        db.user.insert_one({"_id" : profile, "frequenceFriends" : profiles[profile]['frequenceFriends'], "frequenceTweet" : profiles[profile]['frequenceTweet'], "agressivity" : profiles[profile]['agressivity']})
    else :
        db.user.update_one({"_id" : profile},{"$set": {"frequenceFriends" : profiles[profile]['frequenceFriends'],"frequenceTweet" : profiles[profile]['frequenceTweet'], "agressivity" : profiles[profile]['agressivity']}})

        
            
        
