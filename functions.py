#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Functions
# AUTHORS		  : Benjamin GIRALT & Guillaume HANOTEL
# DATE            : 26/02/2018
# ====================================================

import os
import datetime
import colors
import yaml
import sys


def touch(path) -> None:
    """
    Crée le fichier dont le chemin est passé est paramètre
    """
    with open(path, 'a'):
        os.utime(path, None)


def clear_screen() -> None:
    """
    Efface la console
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date() -> str:
    """
    Fonction retournant la date du jour
    :return: formatted_date
    """
    date_now = datetime.datetime.now()
    formatted_date = str(date_now.year) + reformat_number(str(date_now.month)) + reformat_number(str(date_now.day)) + reformat_number(str(date_now.hour)) + reformat_number(str(date_now.minute)) + reformat_number(str(date_now.second))
    return formatted_date


def reformat_number(str_number) -> str:
    """
    Prend en paramètre un nombre (str), si il est inférieur à 10
    rajoute un 0 au début du str
    """
    if int(str_number) < 10:
        str_number = "0" + str_number
    return str_number


def load_config(config_file):
    """
    Prend en paramètre le chemin du fichier de configuration ;
        si il n'existe pas, il le crée et le rempli avec des valeurs par défaut
        si il existe, test si tous les attributs sont bien remplis
    Si tout va bien, la configuration est chargée, sinon dire qu'il faut bien remplir la conf
    """
    if not os.path.exists(config_file):
        print(colors.RED + "File" + config_file + " not found"+ colors.ESCAPE)
        print(colors.CYAN + "Creating " + colors.ESCAPE + config_file + colors.CYAN + " now...\n\n" + colors.ESCAPE)
        touch(config_file)
        fill_default_config_file(config_file)
    else:
        check_config_file(config_file)

    with open(config_file, 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config


def check_config_file(config_file):
    """
    Prend en paramètre le fichier de configuration, et vérifie si les infos sont bien remplis, sinon exit
    """
    with open(config_file, 'r') as ymlfile:
        config = yaml.load(ymlfile)

    param_to_test = [config['mysql']['user'], config['mysql']['host'], config['backup']['backup_folder']]

    # si l'un des param est vide ou si le chemin du backup folder n'existe pas
    if check_emptiness(param_to_test) or not os.path.exists(config['backup']['backup_folder']):
        print("The configuration file is incomplete or the backup folder doesn't exist, please check your parameter in " + config_file)
        sys.exit(0)


def check_emptiness(list):
    for val in list:
        if val == "" or val is None:
            return True
    return False


def fill_default_config_file(config_file) -> None:
    """
    Ouvre le fichier de configuration et le rempli avec une config par défaut
    """
    with open(config_file, 'a') as ymlfile:
        ymlfile.write("mysql:\n")
        ymlfile.write("    host: localhost\n")
        ymlfile.write("    user: root\n")
        ymlfile.write("    passwd: erty\n")
        ymlfile.write("backup:\n")
        ymlfile.write("    backup_folder: /home/vagrant/Documents/\n")

