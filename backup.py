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

import subprocess
import os
import sys
from os.path import expanduser
import ansi_colors as colors
import shutil
import datetime
import yaml
import re
import zipfile


# TODO : Installation du script (PHPMYADMIN)
# TODO : print out requirements.txt

# TODO : droits user mysql : select & lock tables



'''
 ==== Functions ====
'''


def touch(path) -> None:
	"""
	Crée le fichier dont le chemin est passé est paramètre
	"""
	with open(path, 'a'):
		os.utime(path, None)


def mkdir(directory) -> None:
	"""
	Crée le dossier dont le chemin est passé ets paramètre
	"""
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except Exception:
		sys.stderr.write("{}\nError when creating {}\n\n{}".format(colors.RED, directory, colors.ESCAPE))
		sys.exit(1)


def clear_screen() -> None:
	"""
	Efface la console
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


def get_date() -> str:
	"""
	Fonction retournant la date du jour
	"""
	date_now = datetime.datetime.now()
	formatted_date = str(date_now.year) + reformat_number(str(date_now.month)) + reformat_number(
		str(date_now.day)) + reformat_number(str(date_now.hour)) + reformat_number(
		str(date_now.minute)) + reformat_number(str(date_now.second))
	return formatted_date


def reformat_number(str_number) -> str:
	"""
	Prend en paramètre un nombre (str), si il est inférieur à 10
	rajoute un 0 au début du str
	"""
	if int(str_number) < 10:
		str_number = "0" + str_number
	return str_number


def get_existing_dumps(db_name):
	""""
	Prend en paramètre le nom d'une DB, et retourne tous les dumps de celle ci
	"""
	dumps = os.listdir(BACKUP_FOLDER)
	regex = re.compile(db_name+".sql.zip$")
	dumps = list(filter(regex.search, dumps))
	return dumps


def get_oldest_dump(list_dumps):
	"""
	Retourne le plus vieux dump d'une liste de dump
	"""
	return min(list_dumps)


def clean_old_save():
	"""
	Supprime tous les vieux dumps de chaque DB pour en garder au maximum le nombre
	fourni dans la configuration
	"""
	databases = get_list_own_db()
	for database in databases:
		dumps = get_existing_dumps(database)
		while len(dumps) > NB_MAX_SAVE:
			oldest_dump = get_oldest_dump(dumps)
			dumps.remove(oldest_dump)
			os.remove(oldest_dump)


def load_config(config_file):
	"""
	Prend en paramètre le chemin du fichier de configuration ;
		si il n'existe pas, il le crée et le rempli avec des valeurs par défaut
		si il existe, test si tous les attributs sont bien remplis
	Si tout va bien, la configuration est chargée, sinon dire qu'il faut bien remplir la conf
	"""
	if not os.path.exists(config_file):
		print(colors.RED + "File" + config_file + " not found" + colors.ESCAPE)
		print(colors.CYAN + "Creating " + colors.ESCAPE + config_file + colors.CYAN + " now...\n\n" + colors.ESCAPE)
		touch(config_file)
		fill_config_file(config_file)
	else:
		check_config_file(config_file)

	with open(config_file, 'r') as ymlfile:
		config = yaml.load(ymlfile)
	return config


def check_config_file(config_file):
	"""
	Prend en paramètre le fichier de configuration, et vérifie si les infos sont bien remplies, sinon exit
	"""
	with open(config_file, 'r') as ymlfile:
		config = yaml.load(ymlfile)

	param_to_test = [config['mysql']['user'], config['mysql']['host'], config['backup']['backup_folder'],
					 config['backup']['nb_max_save']]

	# si le chemin du backup folder n'existe pas
	mkdir(config['backup']['backup_folder'])

	# si l'un des param est vide
	if check_emptiness(param_to_test):
		print(
			"The configuration file is incomplete, please check your parameter in {} " + config_file + "{}".format(
				colors.CYAN, colors.ESCAPE))
		sys.exit(0)


def check_emptiness(mylist: list) -> bool:
	"""
	Prend en pramètre une liste et renvoie vrai si chacun de ses éléments est à None ou est vide
	"""
	for val in mylist:
		if val == "" or val is None:
			return True
	return False


def ask_config(sentence):
	"""
	Input config
	"""
	while True:
		try:
			param = input(sentence)
			if not param:
				raise ValueError('empty string')
			else:
				return param
		except ValueError as e:
			print(e)


def fill_config_file(config_file) -> None:
	"""
	Ouvre le fichier de configuration et le rempli avec une config par défaut
	"""
	home = expanduser("~")
	backup_dir = home + '/database_backup'

	mkdir(backup_dir)

	print('Please fill your creditentials :')
	host = ask_config("Please enter your host : > ")
	user = ask_config("Please enter your mysql user : > ")
	passwd = ask_config("Please enter your mysql password : > ")
	nb_max_save = ask_config("Please enter the maximum number of saves you want to keep : > ")

	print("Your backup files are stored in {}".format(backup_dir))

	with open(config_file, 'a') as ymlfile:
		ymlfile.write("mysql:\n")
		ymlfile.write("    host: {}\n".format(host))
		ymlfile.write("    user: {}\n".format(user))
		ymlfile.write("    passwd: {}\n".format(passwd))
		ymlfile.write("backup:\n")
		ymlfile.write("    backup_folder: {}\n".format(backup_dir))
		ymlfile.write("    nb_max_save: {}\n".format(nb_max_save))


def create_archive(db_dump_file):
	"""
	Zip le fichier passé en paramètre
	"""
	zipfile.ZipFile(db_dump_file + '.zip', mode='w').write(db_dump_file)


def get_list_own_db() -> list:
	"""
	Retourne la liste des base de données MySQL sans celles par défaut
	"""
	full_list_db = get_list_db_names()
	unwanted_values = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
	list_db = [x for x in full_list_db if x not in unwanted_values]

	return list_db


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


def print_list_db(list_db) -> None:
	"""
	Affiche la liste des BDD passée en paramètre
	"""
	print("Your databases are: \n")
	print('\t - %s' % '\n\t - '.join(map(str, list_db)))
	print("\n")


def print_versions_db(db_versions_array) -> None:
	"""
	Affiche les choix disponibles pour les dumps des BDD
	"""
	print("The available versions for this db are :\n")
	for index in range(len(db_versions_array)):
		print('\t' + str(index) + " - " + db_versions_array[index] + '\t' + " saved at " + timestamp_to_date(
			(db_versions_array[index])[0:14]))


def print_choice_db(db_list) -> None:
	"""
	Affiche les choix disponibles pour les bases de données
	"""
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


'''
=== SAVING FUNCTIONS ===
'''


def save_db(db_name) -> str:
	"""
	Sauvegarde de la base de données passée en paramètre
	"""
	current_date = get_date()
	file_name = str(BACKUP_FOLDER) + str(current_date) + "-dump_" + db_name + ".sql"
	file_name_without_path = str(current_date) + "-dump_" + db_name + ".sql"
	os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + db_name + " > " + file_name)

	print(
		colors.GREEN + "\nDatabase " + colors.ESCAPE + db_name + colors.GREEN + " successfully saved in folder " + colors.ESCAPE + colors.YELLOW + BACKUP_FOLDER + colors.ESCAPE + colors.GREEN + " under the name : " + colors.ESCAPE + file_name_without_path + "\n")

	return file_name


def save_a_single_database(db_name):
	dump_name = save_db(db_name)
	create_archive(dump_name)
	os.remove(dump_name)


def save_all_db() -> None:
	"""
	Sauvegarde de toutes les bases de données
	"""
	# récupérer la liste des archives
	db_list = get_list_own_db()
	for db in db_list:
		save_a_single_database(db)


'''
=== RESTORE FUNCTIONS ===
'''


def restore_db(db_name, db_version) -> None:
	"""
	Restauration de la base de données passée en paramètre
	"""
	# unzip -p dbdump.sql.zip | mysql -u root -p dbname

	backup_file = BACKUP_FOLDER + db_version
	unzip = subprocess.Popen(['unzip', '-p', backup_file], stdout=subprocess.PIPE)

	mysql_command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, '-h', MYSQL_HOST, db_name]

	process = subprocess.Popen(mysql_command, stdin=unzip.stdout)
	process.wait()

	print("{}\nVersion successfully restored.\n{}".format(colors.GREEN, colors.ESCAPE))


def restore_a_single_database(db_name):
	array_all_versions_db = get_list_db_versions(db_name)
	version_chosen = choose_version(array_all_versions_db)
	restore_db(db_name, version_chosen)


def restore_all_db() -> None:
	databases = get_list_own_db()
	for database in databases:
		clear_screen()
		print("{}RESTORE ALL YOUR DATABASES\n{}".format(colors.VIOLET, colors.ESCAPE))
		restore_a_single_database(database)


def choose_db() -> str:
	"""
	Affiche la liste des BDD, et permet à l'utilisateur de choisir celle qu'il veut
	"""
	db_list = get_list_own_db()

	while True:

		print("Your databases are : \n")
		print_choice_db(db_list)

		str_input_choice_db = "{}\nEnter the number matching the database you want to choose: {}\n> ".format(colors.CYAN,
																											colors.ESCAPE)
		db_choice = input(str_input_choice_db)

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
	"""
	Affiche la liste des dumps d'une BDD, et permet à l'utilisateur de choisir celle qu'il veut
	"""
	while True:
		print_versions_db(array_all_versions_db)

		str_input_choice_version = "{}\nPlease select enter the number matching the version of database you want to restore : \n{}> ".format(
			colors.CYAN, colors.ESCAPE)
		version_choice = input(str_input_choice_version)

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


def get_list_db_versions(db_chosen="dump_all_db") -> list:
	"""
	Retourne la liste des dumps de la BDD passé en paramètre
	"""
	# define the ls command
	ls = subprocess.Popen(["ls", "-p", BACKUP_FOLDER],
						  stdout=subprocess.PIPE,
						  )

	# define the grep command
	grep = subprocess.Popen(["grep", db_chosen + '.sql.zip'],
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
	"""
	Lance l'action que l'utilisateur a demandé
	"""
	clear_screen()

	# List databases
	if user_choice == 1:

		print("{}LIST OF YOUR DATABASES\n{}".format(colors.VIOLET, colors.ESCAPE))
		list_db = get_list_own_db()
		print_list_db(list_db)

	# Save all databases
	elif user_choice == 2:
		print("{}SAVE ALL YOUR DATABASES\n{}".format(colors.VIOLET, colors.ESCAPE))
		save_all_db()

	# Restore all databases
	elif user_choice == 3:
		restore_all_db()

	# Save a single database
	elif user_choice == 4:

		print("{}SAVE A SINGLE DATABASE\n{}".format(colors.VIOLET, colors.ESCAPE))
		db_chosen = choose_db()
		save_a_single_database(db_chosen)

	# Restore a single database
	elif user_choice == 5:

		print(colors.VIOLET + "RESTORE A SINGLE DATABASE\n" + colors.ESCAPE)
		db_chosen = choose_db()
		restore_a_single_database(db_chosen)

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
	clean_old_save()



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

clear_screen()
config = load_config(config_file)

MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['passwd']
MYSQL_HOST = config['mysql']['host']
BACKUP_FOLDER = config['backup']['backup_folder']
NB_MAX_SAVE = config['backup']['nb_max_save']

if BACKUP_FOLDER[-1:] != "/":
	BACKUP_FOLDER = BACKUP_FOLDER + "/"

try:
	main()
except KeyboardInterrupt:
	print('\nProcess Interrupted')
	try:
		sys.exit(0)
	except SystemExit:
		sys.exit(0)
