#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Save All DB
# DESCRIPTION     :
# - Sauvegarde de l'ensemble des bases de données présentes sur le serveur
# AUTHORS		  : Benjamin GIRALT & Guillaume HANOTEL
# DATE            : 26/02/2018
# ====================================================

from os.path import expanduser
import colors
import functions as fct
import subprocess
import sys


def save_all_db(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, BACKUP_FOLDER) -> None:
	"""
	Sauvegarde de toutes les bases de données
	"""
	command = ['mysqldump', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, '-h', MYSQL_HOST, '--all-databases', '--events']

	current_date = fct.get_date()
	file_name = str(BACKUP_FOLDER) + current_date + "-dump_all_db.sql"
	file_name_without_path = current_date + "-dump_all_db.sql"

	fct.touch(file_name)
	f = open(file_name, "w")

	return_code = subprocess.call(command, stdout=f)

	fct.clear_screen()
	colors.print_cyan("Saving all your databases...\n")

	if return_code == 0:
		print(colors.GREEN + "Databases successfully saved in: " + colors.YELLOW + str(
			BACKUP_FOLDER) + colors.ESCAPE + colors.GREEN + " under the name : " + colors.ESCAPE + file_name_without_path)
		print(" ")
	else:
		sys.stderr.write("Error Code : " + str(return_code))
		sys.exit(1)


home = expanduser("~")
config_file = home+"/.backup_db_config.yml"
config = fct.load_config(config_file)


MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['passwd']
MYSQL_HOST = config['mysql']['host']
BACKUP_FOLDER = config['backup']['backup_folder']

save_all_db(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, BACKUP_FOLDER)


