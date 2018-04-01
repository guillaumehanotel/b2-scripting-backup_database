
# Projet Database Save Script (Debian 8)
Benjamin GIRALT - Guillaume HANOTEL


## Le projet comporte 2 parties :
1) L'installation d'un environnement permettant la mise en place d'un site web demo
2) Le script de sauvegarde de base de données qui pourra éventuellement utiliser le site de demo pour montrer ses fonctionnalités

## Présentation du projet :
### Partie 1 :
Mise en place d'un serveur web avec : 
- Apache2
- MySQL
- PHP
- phpMyAdmin

### Partie 2 :
Création d'un script python permettant :
- De sauvegarder le serveur MySQL dans une archive compressée 
- De restaurer le serveur MySQL avec une sauvegarde spécifique 
- De supprimer des sauvegardes au-delà d’une certaine limite


## Prérequis :
 Pour installer et faire fonctionner correctement le projet, vous aurez besoin :
 - D'opérer sur un système Debian 8
 - D'un accès root sur votre système
 - D'un accès à l'utilisateur MySQL  : root
 - De la commande sudo


## Installation :

### Etape 1 : Update
   Veillez à ce que votre système soit à jour avec les commandes :

        sudo apt-get update
        sudo apt-get upgrade -y

### Etape 2 : Installation Git

   Veillez à installer Git si ce n'est pas déjà fait

        sudo apt-get install git -y


### Etape 3 : Clone du projet 

   Cloner le projet

        git clone https://github.com/jonimofo/postgreSQL

