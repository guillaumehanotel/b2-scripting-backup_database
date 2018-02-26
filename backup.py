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


def print_choice_db(bdd_list) -> None:
	for index in range(len(bdd_list)):
		print('\t'+str(index)+" - "+bdd_list[index])


def save_db(database_name) -> None:
	"""
	Sauvegarde de la base de données passée en paramètre
	"""
	current_date = get_date()
	file_name = str(BACKUP_FOLDER)+str(current_date)+"-dump_" + database_name + ".sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + database_name + " > "+ file_name)

	print("base "+database_name+" saved in folder "+BACKUP_FOLDER)


def save_all_db() -> None:
	"""
	Sauvegarde de toutes les bases de données
	"""
	command = ['mysqldump', '-u', MYSQL_USER, '-p'+MYSQL_PASSWORD, '--all-databases', '--events']

	current_date = get_date()
	file_name = str(BACKUP_FOLDER)+current_date+"-dump_all_db.sql"

	touch(file_name)
	f = open(file_name, "w")

	return_code = subprocess.call(command, stdout=f)

	# error_code = os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " --all-databases --events > " + file_name)

	if return_code == 0:
		print("Save succesfully stored in "+str(BACKUP_FOLDER))
	else:
		sys.stderr.write("Error Code : " + str(return_code))
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


def choose_db() -> str:
	bdd_list = get_list_own_bdd()

	while True:
		
		print("Voici la liste de vos bases de donnees : \n")

		print_choice_db(bdd_list)
		
		db_choice = input("\nEntrez le numero correspondant a la base que vous souhaitez sauvegarder :\n")
		
		if db_choice.isdigit():
			db_choice = int(db_choice)
			if 0 <= db_choice < len(bdd_list):
				break
			else:
				print("Invalid index")
		else:
			print("Invalid index, please enter a valid index")
		
	db_chosen = str(bdd_list[db_choice])
	print("Vous avez selectionne la base : "+db_chosen)
	return db_chosen


# def save_BDD_zip() -> None:
# 	# Sauvegarde de la BDD compressé :
# 	os.system('mysqldump -u appli_web -p appli_web | gzip -9 > dump_appli_web_01.sql.gz')

# def restore_BDD_from_zip() -> None:
# 	# Restauration de la BDD avec fichier compressé :
# 	os.system('gunzip < dump_appli_web_01.sql.gz | mysql -u appli_web -p appli_web')

def process_user_choice(user_choice) -> None:
	
	cls()
	
	# Liste
	if user_choice == 1:
		
		list_bdd = get_list_own_bdd()
		print_list_bdd(list_bdd)

	# Sauvegarde All
	elif user_choice == 2:
		print("\nSauvegarde de l'ensemble des bases de donnees...")
		save_all_db()
		

	# Restauration All
	elif user_choice == 3:
		"""
		- Regarder dans le dossier des sauvegardes si il y a des sauvegardes concernant 
		l'ensemble des base de données, 
		- si c'est le cas, proposer laquelle restaurer
		- si ce n'est pas le cas, proposer de rentrer le chemin du fichier manuellement
		"""
		restore_all_db()


	## BENJI
	# Sauvegarde Unique
	elif user_choice == 4:

		print("Sauvegarde d'une seule base de donnees \n")
		db_chosen = choose_db()
		save_db(db_chosen)


	# Restauration Unique
	elif user_choice == 5:
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
		user_choice = int(input("Votre choix ?\n> "))
	except ValueError:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)

	process_user_choice(user_choice)


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




