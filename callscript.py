#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import os
import subprocess

var = 'toto'

# rc = subprocess.call("/vagrant/postgreSQL/set_crontab.sh %s" % (str(var)), shell=True)

def touch(path) -> None:
    """
    Crée le fichier dont le chemin est passé est paramètre
    ex : touch('/home/toto.txt')
    """
    with open(path, 'a'):
        os.utime(path, None)


touch('/vagrant/postgreSQL/AAAAAAA.txt')
touch('/home/vagrant/AAAAAAA.txt')


