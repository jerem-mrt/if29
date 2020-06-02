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
# On execute la requête et pour chacun des tweets, on conserve les données qui nous intéressent
for tweet in tweets:
    # Si l'utilisateur n'a pas encore été rencontré, on l'ajoute à notre dictionnaire profiles
    if tweet['user']['id'] not in profiles :
        profiles[tweet['user']['id']] = {}
        profiles[tweet['user']['id']]['timestamp'] = []
        profiles[tweet['user']['id']]['timestamp'].append(int(tweet['timestamp_ms']))
        nbLinks = len(tweet['entities']['urls'])
        profiles[tweet['user']['id']]['outgoing_link'] = nbLinks
    # Sinon on ajoute l'id d'utilisateur au dictionnaire profiles
    else :
        profiles[tweet['user']['id']]['timestamp'].append(int(tweet['timestamp_ms']))
        profiles[tweet['user']['id']]['outgoing_link'] = profiles[tweet['user']['id']]['outgoing_link'] + nbLinks
        
print("Parcours des utilisateurs fini")

# On détermine l'agressivité de chacun des profiles
for profile in profiles:
    profiles[profile]['timestamp'].sort(reverse=True)
    timestamp = np.array(profiles[profile]['timestamp'])
    profiles[profile]['frequenceTweet'] = 0
    # S'il y a plus d'un tweet de retenu, on additionne les écarts entre chaque tweet
    if len(timestamp) > 1:
        for i in range(0, len(timestamp)-1):
            if timestamp[i-1] == timestamp[i]:
            
                profiles[profile]['frequenceTweet'] = profiles[profile]['frequenceTweet'] + 2
            profiles[profile]['frequenceTweet'] = profiles[profile]['frequenceTweet'] + (int(timestamp[i]) - int(timestamp[i + 1]))
        #On convertit l'écart en ms en écart en heure
        frequence = profiles[profile]['frequenceTweet'] / 3600000
        profiles[profile]['frequenceTweet'] = (len(timestamp)-1) / frequence
        profiles[profile]['agressivity'] = (profiles[profile]['frequenceTweet'] + profiles[profile]['outgoing_link']) / 350
    else :
        profiles[profile]['agressivity'] = profiles[profile]['outgoing_link'] / 350
