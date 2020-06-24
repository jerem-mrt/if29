import numpy as np
from pprint import pprint
# Prérequis : pymongo et sshtunnel (pip install pymongo sshtunnel), il est aussi possible de lancer le script depuis
# le serveur devisi en ssh mais plus complexe pour les non initiés au bash/ssh

from sshtunnel import SSHTunnelForwarder
from getpass import getpass
import pymongo

hostname = "dev-isi.utt.fr"
username = input("marottej")
ssh_pass = getpass("Lent=1195*MJ")
mongo_username = input("lambda_student")
mongo_pass = getpass("password")

# Forwarding SSH
server = SSHTunnelForwarder(hostname, ssh_username=username, ssh_password=ssh_pass, remote_bind_address=('127.0.0.1', 27017))
server.start()

# Client mongo
client = pymongo.MongoClient('127.0.0.1', server.local_bind_port, username=mongo_username, password=mongo_pass, authSource="if29") # server.local_bind_port is assigned local port
db = client["if29"]

# VOTRE CODE ICI :)
# On se concentre sur la Collection Tweets : on récupère l'ensemble des tweets
tweets = db.tw10.find()
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


# Fermeture du serveur SSH et du client Mongo, à garder pour que le programme s'arrête tout seul :)
client.close()
server.close()