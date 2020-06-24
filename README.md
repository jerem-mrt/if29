	README - Comparaison de deux méthodes de classification de profils de Twitter - Projet IF29


DESCRIPTION : 
Ce projet permet de calculer différents indices (agressivité, visibilité, ...) qui caractérisent des tweets 
d'une base de données et de les répartir selon des clusters afin de séparer les tweets malveillants des autres.
Pour ce faire, nous utilisons deux algorithmes : 
	- k-means (non-supervisé)
	- SVM (supervisé)
Nous faisons tout cela dans le but de comparer les deux algorithmes pour savoir quel est le plus adapté à la 
situation donnée.


UTILISATION : 
1. Il faut avoir une base de données nommée IF29 avec une collection de tweets nommée tweet 
et une autre nommée user qui sera remplie après.

2. Se placer dans le répertoir de travail

3. Afin d'utiliser le code, il faut d'abord installer les modules suivants : 
	- pymongo
	- numpy
	- pprint
	- datetime
	- sklearn
	- matplotlib
Pour installer ces modules vous pouvez utiliser la commande suivante:
>> pip install nomModule

4. Pour calculer les indices à analyser écrivez dans la ligne de commande : 
>> python nomFichier
Les fichiers concernés sont : 
	- agressivite.py
	- fonction_longueur_tweets.py
	- kmeans_visi_agressivite.py
	- nbfollowers_nbprofilsSuivis_ratio.py
	- visibilite.py
Les changements seront disponnibles dans la table user 

5. Afin d'appeler les deux alogrithmes de clustering écrivez dans la ligne de commande : 
>> python nomFihchier
les fichiers concernés sont : 
	- kmeans_visi_agressitive.py
	- svm_agr_visi.py
Le graphique avec les clusters s'affichera.








CONTACTS :
alizee.tana@utt.fr
elise.poignant@utt.fr
callista.spiteri@utt.fr
jeremie.marotte@utt.fr
thomas.mougin@utt.fr