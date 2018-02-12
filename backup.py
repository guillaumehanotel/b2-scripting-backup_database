#!/usr/bin/python3.4
from subprocess import call
import os


#call(["ls", "-l"])


def save_BDD():
	# Sauvegarde de la BDD :
	os.system('mysqldump -u appli_web -p appli_web > dump_appli_web_01.sql')

def save_BDD_zip():
	# Sauvegarde de la BDD compressé :
	os.system('mysqldump -u appli_web -p appli_web | gzip -9 > dump_appli_web_01.sql.gz')

def restore_BDD():
	# Restauration de la BDD :
	os.system('mysql -u appli_web -p appli_web < dump_appli_web_01.sql')

def restore_BDD_from_zip():
	# Restauration de la BDD avec fichier compressé :
	os.system('gunzip < dump_appli_web_01.sql.gz | mysql -u appli_web -p appli_web')


restore_BDD()