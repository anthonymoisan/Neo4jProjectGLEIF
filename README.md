# Neo4jProjectGLEIF

L'objectif de ce projet est l'utilisation de Neo4j, base de données orientées Graph sur la consolidation des entités à travers le Global Legal Entity Identifier

La GLEIF [lien](https://www.gleif.org) met à disposition le Répertoire mondial des LEI, la seule source mondiale en ligne de données de référence ouvertes, normalisées et de haute qualité sur les entités juridiques.

## Pour démarrer

Il suffit de cloner ou copier en local le répetoire.

L'organisation du dépot est la suivante :
* le Notebook Jupyter dans src qui permet de s'interfacer avec Neo4j via py2neo pour lancer les requêtes Cypher, d'incorporer des images et du texte pour expliciter le travail.  
* les requêtes Cypher dans scriptCypher pour les personnes qui souhaitent uniquement évoluer dans l'environnement Neo4j
* les données converties dans data
* un convertisseur est aussi incorporé dans src pour extraire à partir des données volumineuses les données utiles pour notre modélisation

## Versioning

Nous utilisons Github pour le versionning. 

## Auteur

**Anthony Moisan** **Leonard Péan**- *Initial work @04/12/2019* 

## Licence

Ce projet est sous licence MIT voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails


