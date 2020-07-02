	README - Comparaison de deux m�thodes de classification de profils de Twitter - Projet IF29



DESCRIPTION : 
Ce projet permet de calculer diff�rents indices (agressivit�, visibilit�, ...) qui caract�risent des tweets 
d'une base de donn�es et de les r�partir selon des clusters afin de s�parer les tweets malveillants des autres.
Pour ce faire, nous utilisons trois algorithmes : 
	- k-means (non-supervis�)
	- DBscan (non-supervis�)
	- SVM (supervis�)
Nous faisons tout cela dans le but de comparer deux algorithmes pour savoir quel est le plus adapt� � la situation donn�e.





UTILISATION : 
1. Il faut avoir une base de donn�es MongoDB nomm�e IF29 avec une collection de tweets nomm�e "tweet" 
et une autre nomm�e "user".

2. Se placer dans le r�pertoire de travail

3. Afin d'utiliser le code, il faut d'abord installer les modules suivants : 
	- pymongo
	- numpy
	- pprint
	- datetime
	- sklearn
	- matplotlib
Pour installer ces modules vous pouvez utiliser la commande suivante :
>> pip install nomModule

4. Pour calculer les indices � analyser d�placez vous dans le dossier indicateur et �crivez dans la ligne de commande : 
>> python nomFichier
Les fichiers concern�s sont : 
	- agressivite.py
	- fonction_longueur_tweets.py
	- kmeans_visi_agressivite.py
	- nbfollowers_nbprofilsSuivis_ratio.py
	- visibilite.py
	- outgoing_link.py
Les changements seront disponibles dans la table user 

5. Pour repr�senter tous les indices dans un graphiques, nous utilisons l'ACP : 
>> python PCA.py
Il faut avoir calcul� tous les indices avant de le lancer.
Vous verrez un changement dans la base MongoDB (les composantes principales PC1 et 
PC2 ont �t� rajout�es).

6. Afin d'appeler les deux algorithmes de clustering non supervis�s, allez dans le r�pertoire correspondant 
(dbscan ou kmeans) et �crivez dans la ligne de commande : 
>> python nomFihchier
les fichiers concern�s sont : 
	- kmeans_ACP.py
	- dbscan_ACP.py
Le graphique avec les clusters s'affichera.
Si vous voulez d'abord savoir quel epsilon choisir avant de lancer le dbscan, lancez calcul_eps.py. 

7. Pour appeler l'algorithme de clustering supervis� il faut d'abord lab�liser une portion des individus : 
	- allez dans le r�pertoire labels 
	- �crivez : >> python swm_agr_visi.py
Puis, aller dans le r�pertoire svm �crire : 
	>> python labeliser.py
	>> python svm_ACP.py
Le graphique avec les clusters s'affichera.






CONTACTS :
alizee.tana@utt.fr
elise.poignant@utt.fr
callista.spiteri@utt.fr
jeremie.marotte@utt.fr
thomas.mougin@utt.fr
