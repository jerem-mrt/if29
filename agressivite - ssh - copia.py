import numpy as np
from pprint import pprint
# Prérequis : pymongo et sshtunnel (pip install pymongo sshtunnel), il est aussi possible de lancer le script depuis
# le serveur devisi en ssh mais plus complexe pour les non initiés au bash/ssh

from sshtunnel import SSHTunnelForwarder
from getpass import getpass
import pymongo

hostname = "dev-isi.utt.fr"
username = input("Nom d'utilisateur UTT : ")
ssh_pass = getpass("Mot de passe UTT : ")
mongo_username = input("Nom d'utilisateur MongoDB : ")
mongo_pass = getpass("Mot de passe MongoDB : ")
# Forwarding SSH
server = SSHTunnelForwarder(hostname, ssh_username=username, ssh_password=ssh_pass, remote_bind_address=('127.0.0.1', 27017))
server.start()
print("connection initiée")
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

client.close()
server.close()
