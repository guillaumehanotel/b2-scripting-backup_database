#!/usr/bin/python3.4
from subprocess import call
import os
import datetime

# db are stored in : /var/lib/mysql


##### Variables
current_date = datetime.date.today()
backup_folder = "/home/vagrant/Documents"


##### Functions
def save_db():
	# Sauvegarde de la BDD :
	os.system('mysqldump -u root -perty appli_web > /home/vagrant/Documents/dump_appli_web_01.sql')

def save_all_db():
	# Sauvegarde toutes les BDD :
	os.system('mysqldump -u root -perty --all-databases --events >' +str(backup_folder)+str(current_date)+'-dump_all_db_01.sql')


# def save_BDD_zip():
# 	# Sauvegarde de la BDD compressé :
# 	os.system('mysqldump -u appli_web -p appli_web | gzip -9 > dump_appli_web_01.sql.gz')

def restore_all_db():
	# Restauration des BDD :
	os.system('mysql -u root -p appli_web < dump_appli_web_01.sql')


# def restore_BDD_from_zip():
# 	# Restauration de la BDD avec fichier compressé :
# 	os.system('gunzip < dump_appli_web_01.sql.gz | mysql -u appli_web -p appli_web')



##### Main
choix_user = input("Bienvenue dans l'utilitaire de gestion de base de données.\n\n\tTapez 1 pour sauvegarder l'ensemble de vos base de données.\n\tTapez 2 pour restaurer vos bases de donnees.\n")

if  choix_user == "1":
	print("\nSauvegarde de l'ensemble des bases de donnees...")
	save_all_db()
else:
	print("toto")



