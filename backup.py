#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Database Save Manager
# DESCRIPTION     : 
#		- Sauvegarde de l'ensemble des bases de données présentes sur le serveur
#		- Restauration de la sauvegarde
#		- Gérer la rétention des sauvegardes (fichier de config)
#		- BONUS : Restaurer un backup précis avec une base de données précise
#		- BONUS : Chiffrement de la sauvegarde
# AUTHORS		  : Benjamin GIRALT & Guillaume HANOTEL
# DATE            : 26/02/2018
# ====================================================

"""
QUESTIONS / INTERROGATIONS :

	- Laisser la possibilité de nommer une sauvegarde ?
	- Laisser la possibilité de faire des saves zippés ?


"""


import subprocess
import os
import sys
import datetime

# Databases are stored in : /var/lib/mysql

##### Constantes # TODO : à externaliser dans un fichier de conf
MYSQL_USER = "root"
MYSQL_PASSWORD = "erty"


##### Functions

def cls() -> None:
    os.system('cls' if os.name=='nt' else 'clear')


def get_date() -> str:
    """
    Fonction retournant la date du jour
    :return: formatted_date
    """
    now = datetime.datetime.now()
    formatted_date = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    return formatted_date


def get_list_bdd() -> list:

	command = "mysql -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " -e 'show databases;'"

	# output bash to python variable
	proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
	(out, err) = proc.communicate()
	output = out.decode(encoding='utf-8')

	full_list_bdd = output.split("\n")
	full_list_bdd = list(filter(None, full_list_bdd))

	unwanted_values = ['Database', 'information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
	list_bdd = [x for x in full_list_bdd if x not in unwanted_values]

	return list_bdd


def save_db(database_name) -> None:
	"""
	Sauvegarde de la base de données passée en paramètre
	"""
	current_date = get_date()
	file_name = str(backup_folder)+str(current_date)+"-dump_" + database_name + ".sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + database_name + " > "+ file_name)


def save_all_db() -> None:
	"""
	Sauvegarde de toutes les bases de données
	"""
	current_date = get_date()
	file_name = str(backup_folder)+current_date+"-dump_all_db.sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " --all-databases --events > " + file_name)



def restore_db(database_name) -> None:
	"""
	Restauration de la base de données passée en paramètre
	"""
	#os.system("mysql -u root -p " + database_name + " < dump_appli_web_01.sql")
	pass

def restore_all_db() -> None:
	"""
	Restauration de toutes les bases de données
	"""
	pass


# def save_BDD_zip() -> None:
# 	# Sauvegarde de la BDD compressé :
# 	os.system('mysqldump -u appli_web -p appli_web | gzip -9 > dump_appli_web_01.sql.gz')

# def restore_BDD_from_zip() -> None:
# 	# Restauration de la BDD avec fichier compressé :
# 	os.system('gunzip < dump_appli_web_01.sql.gz | mysql -u appli_web -p appli_web')

def process_user_choice(choix_user) -> None:
	# Liste
	if choix_user == 1:
		
		list_bdd = get_list_bdd()
		print(list_bdd)

	# Sauvegarde All
	elif choix_user == 2:
		print("\nSauvegarde de l'ensemble des bases de donnees...")
		save_all_db()

	# Restauration All
	elif choix_user == 3:
		"""
		- Regarder dans le dossier des sauvegardes si il y a des sauvegardes concernant 
		l'ensemble des base de données, 
		- si c'est le cas, proposer laquelle restaurer
		- si ce n'est pas le cas, proposer de rentrer le chemin du fichier manuellement
		"""
		restore_all_db()


	# Sauvegarde Unique
	elif choix_user == 4:
		"""
		- Lister les base de données dispo
		- Demander laquelle sauvegarder
		- Sauvegarder celle demandée
		"""	
		database_name = None
		save_db(database_name)


	# Restauration Unique
	elif choix_user == 5:
		"""
		- Lister les base de données dispo
		- Demander laquelle sauvegarder
		- Regarder dans le dossier des sauvegardes si il y a des sauvegardes concernant 
		la bdd voulu
		- si c'est le cas, proposer laquelle restaurer
		- si ce n'est pas le cas, proposer de rentrer le chemin du fichier manuellement
		"""
		database_name = None
		restore_db(database_name)

	else:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)




##### Variables
backup_folder = "/home/vagrant/Documents/"



##### Main
cls()

print("\nBienvenue dans l'utilitaire de gestion de base de données.\n")
print("\tEntrez un nombre correspondant à une action à effectué :\n")
print("\t[1] => Liste de vos bases de donnees.")
print("\t[2] => Sauvegarder l'ensemble de vos base de donnees.")
print("\t[3] => Restaurer l'ensemble de vos bases de donnees.\n")
print("\t[4] => Sauvegarder une base de donnees unique.\n")
print("\t[5] => Restaurer une base de donnees unique.\n")


try:
	choix_user = int(input("Votre choix ?\n> "))
except ValueError:
	sys.stderr.write("Error : Undefined choice\n")
	sys.exit(1)

process_user_choice(choix_user)

