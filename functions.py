#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Functions
# AUTHORS		  : Benjamin GIRALT & Guillaume HANOTEL
# DATE            : 26/02/2018
# ====================================================

import os
import datetime


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