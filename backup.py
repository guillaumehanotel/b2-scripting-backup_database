#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Mysql Database Save Manager
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

	- tester si on est pas sur windows ?
	- tester en premier lieu si mysql est installé ?
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
BACKUP_FOLDER = "/home/vagrant/Documents/"




##### Functions

def touch(path) -> None:
	with open(path, 'a'):
		os.utime(path, None)

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
	"""
	Retourne la liste des base de données MySQL
	"""

	command = "mysql -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " -e 'show databases;'"

	# output bash to python variable
	proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
	(out, err) = proc.communicate()
	output = out.decode(encoding='utf-8')

	full_list_bdd = output.split("\n")
	full_list_bdd = list(filter(None, full_list_bdd))

	unwanted_values = ['Database']
	list_bdd = [x for x in full_list_bdd if x not in unwanted_values]

	return list_bdd

def get_list_own_bdd() -> list:
	"""
	Retourne la liste des base de données MySQL sans celles par défaut
	"""
	full_list_bdd = get_list_bdd()
	unwanted_values = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
	list_bdd = [x for x in full_list_bdd if x not in unwanted_values]

	return list_bdd

def print_list_bdd(list_bdd) -> None:
	print("\n\tListe de vos bases de données : \n")
	print('\t - %s' % '\n\t - '.join(map(str, list_bdd)))
	print("\n")




def save_db(database_name) -> None:
	"""
	Sauvegarde de la base de données passée en paramètre
	"""
	current_date = get_date()
	file_name = str(BACKUP_FOLDER)+str(current_date)+"-dump_" + database_name + ".sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + database_name + " > "+ file_name)


	# mysqldump -u root -perty appli_web > filetest.sql

def save_all_db() -> None:
	"""
	Sauvegarde de toutes les bases de données
	"""
	command = ['mysqldump', '-u', MYSQL_USER, '-p'+MYSQL_PASSWORD, '--all-databases', '--events']

	current_date = get_date()
	file_name = str(BACKUP_FOLDER)+current_date+"-dump_all_db.sql"

	touch(file_name)
	f = open(file_name, "w")

	error_code = subprocess.call(command, stdout=f)

	# error_code = os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " --all-databases --events > " + file_name)

	if error_code == 0:
		print("Save succesfully stored in "+str(BACKUP_FOLDER))
	else:
		sys.stderr.write("Error Code : " + str(error_code))
		sys.exit(1)

	# mysqldump -u root -perty --all-databases --events > filetest.sql


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
		
		list_bdd = get_list_own_bdd()
		print_list_bdd(list_bdd)

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


##### Main
def main():

	cls()

	print("\nBienvenue dans l'utilitaire de gestion de base de donnees.\n")
	print("\tEntrez un nombre correspondant a une action a effectuer :\n")

	print("\t[1] => Liste de vos bases de donnees.")
	print("\t[2] => Sauvegarder l'ensemble de vos base de donnees.")
	print("\t[3] => Restaurer l'ensemble de vos bases de donnees.")
	print("\t[4] => Sauvegarder une base de donnees unique.")
	print("\t[5] => Restaurer une base de donnees unique.\n")


	try:
		choix_user = int(input("Votre choix ?\n> "))
	except ValueError:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)

	process_user_choice(choix_user)


'''
if __name__ == "__main__":
	main()
'''

main()



def test():

	command = ['mysqldump', '-u' ,MYSQL_USER ,'-p'+MYSQL_PASSWORD, 'appli_web']
	path = "/vagrant/postgreSQL/test.sql"
	touch(path)
	f = open(path, "w")
	
	error_code = subprocess.call(command, stdout=f)

	if error_code == 0:
		print("success")
	else:
		print("Error Code : " + str(error_code))


	'''
	try:
		output = subprocess.check_output(command, stdout=f, stderr=subprocess.STDOUT, shell=True, timeout=3,universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		print("Status : FAIL", exc.returncode, exc.output)
	else:
		print("Output: \n{}\n".format(output))
	'''


	'''
	process = subprocess.Popen(command, shell=True,
                           stdout=f, 
                           stderr=subprocess.PIPE)

	# wait for the process to terminate
	out, err = process.communicate()
	errcode = process.returncode
	'''



#test()




