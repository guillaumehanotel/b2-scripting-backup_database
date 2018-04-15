
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
	sudo apt-get install make -y


### Etape 3 : Clone du projet 

   Cloner le projet
	
	cd ~
        git clone https://github.com/jonimofo/postgreSQL

### Partie 1 : Installation du serveur web

Pour installer le serveur web (apache/mysql/php/phpmyadmin) et le site, il faut taper les commandes suivantes :

		cd ~/postgreSQL/script_install
		make server_install
		
Cette commande va installer consécutivement :
- Apache2
- PHP 7.1
- MySQL
	- Lors de l'installation de MySQL, il vous sera  demandé de remplir des champs :
	- Fournir un mot de passe pour le user "root"								
	
			<YOUR_PASSWORD>
			<Tab>
			<Entrer>
	- Répéter le mot de passe choisi :
	
			<YOUR_PASSWORD_REPEATED>
			<Tab>
			<Entrer>
- PHPMyAdmin
 	- Lors de l'installation de PHPMyAdmin, il vous sera  demandé de remplir des champs :
	- Cocher la cache "apache2"								
	
			<Espace>
			<Tab>
			<Entrer>
	- "Configure database for phpmyadmin..." :
	
			<Entrer>
			
	- Fournir un mot de passe pour le compte root	:							
	
			<YOUR_PASSWORD>
			<Tab>
			<Entrer>
	- Fournir un mot de passe pour le compte MySQL	:							
	
			<YOUR_PASSWORD>
			<Tab>
			<Entrer>
	- Confirmer le mot de passe	:							
	
			<YOUR_PASSWORD_REPEATED>
			<Tab>
			<Entrer>

- Le site web, ainsi que la configuration apache associé
- La base de données **appli_web** du site web avec son utilisateur MySQL associé : **appli_web**
	- Il vous sera demandé lors du déploiement de la base de données, le mot de passe MySQL de l'utilisateur **root** :
	
			<YOUR_PASSWORD>
			<Entrer>
			
			
### Partie 2 : Script de sauvegarde

#### Prérequis 
Lors de la première éxecution du script, il vous sera demander de rentrer les identifiants de votre utilisateur MySQL.
Pour que le script fonctionne, il faut bien que l'utilisateur ait un minimum de privilèges pour pouvoir faire des sauvegardes.
Exécutez cette commande en remplaçant par vos informations :

	mysql -u root -p -e 'GRANT SELECT, LOCK TABLES, SHOW DATABASES ON *.* TO <YOUR_USER>@<YOUR_HOST>'


#### Installation du script

Pour installer les dépendances nécessaires à l'exécution du script, tapez les commandes suivantes : 
	
	cd ~/postgreSQL/script_install
	make script_install

#### Usage 
Vous pouvez maintenant utiliser le script de sauvegarde :

	python3 ~/postgreSQL/backup.py

A la première utilisation, celui-ci vous demandera vos identifiants MySQL, ainsi que le nombre maximal de sauvegarde que vous voulez garder par base de donnée.

Les sauvegardes sont par défauts enregistrées dans le dossier **~/database_backup/**

Mais vous pouvez changer tous ces paramètres dans le fichier le configuration présent à ce chemin : **~/.backup_db_config.yml**


