#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Mysql Database Save Manager
# DESCRIPTION     : 
# - Sauvegarde de l'ensemble des bases de données présentes sur le serveur
# - Restauration de la sauvegarde
# - Gérer la rétention des sauvegardes (fichier de config)
# - BONUS : Restaurer un backup précis avec une base de données précise
# - BONUS : Chiffrement de la sauvegarde
# AUTHORS		  : Benjamin GIRALT & Guillaume HANOTEL
# DATE            : 26/02/2018
# ====================================================

"""
QUESTIONS / INTERROGATIONS :

- tester en premier lieu si mysql est installé ?
- Laisser la possibilité de faire des saves zippés ?

"""

import subprocess
import os
import sys
from os.path import expanduser
import ansi_colors as colors
import functions as fct
from save_all_db import save_all_db
import cron_chooser as cron



# TODO : set correct time

# TODO : Installation du script (PHPMYADMIN)
# TODO : print out requirements.txt

# TODO : Demander les identifiants à la 1ere execution du script (afficher ou est le fichier le conf)
# TODO : Rajouter un param pour le nb max de sauvegarde + add fct de delete old save
# TODO : droits user mysql : select & lock tables
# TODO : zipper les sauvegardes


'''
 ==== Functions ====
'''


def alter_db():
	os.system("mysql -u root -perty appli_web -e 'UPDATE user SET user_pseudo = \"satan\" WHERE user_id = 1'")


def select_user():
	os.system("mysql -u root -perty appli_web -e 'SELECT * from user'")


def get_list_db_names() -> list:
	"""
	Retourne la liste des base de données MySQL
	"""

	command = "mysql -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " -h " + MYSQL_HOST + " -e 'show databases;'"

	# output bash to python variable
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(out, err) = process.communicate()
	output = out.decode(encoding='utf-8')

	output_db_list_raw = output.split("\n")
	output_db_list = list(filter(None, output_db_list_raw))

	unwanted_values = ['Database']
	db_name = [x for x in output_db_list if x not in unwanted_values]

	return db_name


def get_list_own_db() -> list:
	"""
	Retourne la liste des base de données MySQL sans celles par défaut
	"""
	full_list_db = get_list_db_names()
	unwanted_values = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
	list_db = [x for x in full_list_db if x not in unwanted_values]

	return list_db


def print_list_db(list_db) -> None:
	print("Your databases are: \n")
	print('\t - %s' % '\n\t - '.join(map(str, list_db)))
	print("\n")


def print_versions_db(db_versions_array) -> None:
	print("The available versions for this db are :\n")
	for index in range(len(db_versions_array)):
		print('\t' + str(index) + " - " + db_versions_array[index] + '\t' + " saved at " + timestamp_to_date(
			(db_versions_array[index])[0:14]))


def print_choice_db(db_list) -> None:
	for index in range(len(db_list)):
		print('\t' + str(index) + " - " + db_list[index])


def timestamp_to_date(date) -> str:
	year = date[0:4]
	month = date[4:6]
	day = date[6:8]
	hour = date[8:10]
	minute = date[10:12]
	second = date[12:14]

	return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second


def save_db(db_name) -> None:
	"""
	Sauvegarde de la base de données passée en paramètre
	"""
	current_date = fct.get_date()
	file_name = str(BACKUP_FOLDER) + str(current_date) + "-dump_" + db_name + ".sql"
	file_name_without_path = str(current_date) + "-dump_" + db_name + ".sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + db_name + " > " + file_name)

	print(
		colors.GREEN + "\nDatabase " + colors.ESCAPE + db_name + colors.GREEN + " successfully saved in folder " + colors.ESCAPE + colors.YELLOW + BACKUP_FOLDER + colors.ESCAPE + colors.GREEN + " under the name : " + colors.ESCAPE + file_name_without_path + "\n")


def restore_db(db_name, db_version) -> None:
	"""
	Restauration de la base de données passée en paramètre
	"""
	command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, '-h', MYSQL_HOST, db_name]

	backup_file = open(BACKUP_FOLDER + db_version)
	process = subprocess.Popen(command, stdin=backup_file)
	process.wait()
	print(colors.GREEN + "\nVersion successfully restored.\n" + colors.ESCAPE)


def restore_all_db(db_version) -> None:
	command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, '-h', MYSQL_HOST]

	backup_file = open(BACKUP_FOLDER + db_version, 'r')
	process = subprocess.Popen(command, stdin=backup_file)
	process.wait()
	print(colors.GREEN + "\nVersion successfully restored.\n" + colors.ESCAPE)


def choose_db() -> str:
	db_list = get_list_own_db()

	while True:

		print("Your databases are : \n")

		print_choice_db(db_list)

		db_choice = input(
			colors.CYAN + "\nEnter the number matching the database your want to save:" + colors.ESCAPE + "\n> ")

		if db_choice.isdigit():
			db_choice = int(db_choice)
			if 0 <= db_choice < len(db_list):
				break
			else:
				print("Invalid index")
		else:
			print("Invalid index, please enter a valid index")

	db_chosen = str(db_list[db_choice])
	print(colors.CYAN + "\nYou selected database : " + colors.ESCAPE + db_chosen)
	return db_chosen


def choose_version(array_all_versions_db) -> str:
	while True:
		print_choice_db(array_all_versions_db)
		version_choice = input(
			colors.CYAN + "\nPlease select enter the number matching the database you want to restore : \n" + colors.ESCAPE + "> ")

		if version_choice.isdigit():
			version_choice = int(version_choice)
			if 0 <= version_choice < len(array_all_versions_db):
				break
			else:
				print("Invalid index")
		else:
			print("Invalid index, please enter a valid index")

	version_chosen = str(array_all_versions_db[version_choice])
	print(colors.CYAN + "\nYou selected version : " + colors.ESCAPE + version_chosen)
	return version_chosen


def get_list_db_versions(db_chosen="dump_all_db"):
	# define the ls command
	ls = subprocess.Popen(["ls", "-p", BACKUP_FOLDER],
						  stdout=subprocess.PIPE,
						  )

	# define the grep command
	grep = subprocess.Popen(["grep", db_chosen + '.sql'],
							stdin=ls.stdout,
							stdout=subprocess.PIPE,
							)

	# read from the end of the pipe (stdout)
	endOfPipe = grep.stdout

	str_all_versions_db = ""

	# output the files line by line
	for line in endOfPipe:
		str_all_versions_db = str_all_versions_db + line.decode('utf-8')

	# split de str_all_versions_db
	if str_all_versions_db == "":
		print("No backup found. Please make one already !")
		sys.exit(1)
	else:
		array_all_versions_db_raw = str_all_versions_db.split('\n')
		array_all_versions_db = list(filter(None, array_all_versions_db_raw))

	print(colors.CYAN + "\nVersions of : " + colors.ESCAPE + db_chosen + "\n")
	return array_all_versions_db


def process_user_choice(user_choice) -> None:
	fct.clear_screen()

	# List databases
	if user_choice == 1:

		print(colors.VIOLET + "LIST OF YOUR DATABASES\n" + colors.ESCAPE)
		list_db = get_list_own_db()
		print_list_db(list_db)

	# Save all databases
	elif user_choice == 2:

		print(colors.VIOLET + "SAVE ALL YOUR DATABASES\n" + colors.ESCAPE)
		save_all_db(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, BACKUP_FOLDER)

	# Restore all databases
	elif user_choice == 3:

		print(colors.VIOLET + "SAVE ALL YOUR DATABASES\n" + colors.ESCAPE)
		array_all_versions_db = get_list_db_versions()
		version_chosen = choose_version(array_all_versions_db)
		restore_all_db(version_chosen)

	# Save a single database
	elif user_choice == 4:

		print(colors.VIOLET + "SAVE A SINGLE DATABASE\n" + colors.ESCAPE)
		db_chosen = choose_db()
		save_db(db_chosen)

	# Restore a single database
	elif user_choice == 5:

		print(colors.VIOLET + "RESTORE ALL YOUR DATABASES\n" + colors.ESCAPE)
		db_chosen = choose_db()
		array_all_versions_db = get_list_db_versions(db_chosen)
		version_chosen = choose_version(array_all_versions_db)
		restore_db(db_chosen, version_chosen)

	elif user_choice == 6:
		exit(0)

	else:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)


'''
 ==== MAIN ====
'''


def main():
	print("Welcome to the database management program.\n")
	print("Please enter the number matching your choice :\n")

	print("\t[1] => {}List{} your databases".format(colors.YELLOW, colors.ESCAPE))
	print("\n\t[2] => {}Save all {}your databases".format(colors.YELLOW, colors.ESCAPE))
	print("\t[3] => {}Restore all{} your databases".format(colors.YELLOW, colors.ESCAPE))

	print("\n\t[4] => {}Save a single{} database".format(colors.YELLOW, colors.ESCAPE))
	print("\t[5] => {}Restore a single{} database".format(colors.YELLOW, colors.ESCAPE))

	print("\n\t[6] => {}Exit{}".format(colors.YELLOW, colors.ESCAPE))

	while True:
		try:
			user_choice = int(input("\n\n{}Enter your choice :{} \n > ".format(colors.CYAN, colors.ESCAPE)))
			break
		except ValueError:
			sys.stderr.write("{}\nError : Undefined choice\n\n{}".format(colors.RED, colors.ESCAPE))
		# sys.exit(1)

	process_user_choice(user_choice)


'''
INSTALLATION PY YAML

tar zxvf PyYAML-3.12.tar.gz 
sudo chown -R $USER /usr/local/lib/python3.4
python3 setup.py install
http://pyyaml.org/wiki/PyYAML
'''

'''
 ==== Constantes ====  
'''
home = expanduser("~")
config_file = home + "/.backup_db_config.yml"

#fct.clear_screen()
config = fct.load_config(config_file)

MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['passwd']
MYSQL_HOST = config['mysql']['host']
BACKUP_FOLDER = config['backup']['backup_folder']

try:
	main()
except KeyboardInterrupt:
	print('\nProcess Interrupted')
	try:
		sys.exit(0)
	except SystemExit:
		sys.exit(0)
