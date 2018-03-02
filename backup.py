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

'''
 ==== Constantes ====  
'''

# TODO : à externaliser dans un fichier de conf
MYSQL_USER = "root"
MYSQL_PASSWORD = "erty"
BACKUP_FOLDER = "/home/vagrant/Documents/"

'''
 ==== Functions ====
'''


def touch(path) -> None:
    with open(path, 'a'):
        os.utime(path, None)


def clear_screen() -> None:
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
    if int(str_number) < 10:
        str_number = "0" + str_number
    return str_number



def get_list_database_names() -> list:
    """
    Retourne la liste des base de données MySQL
    """

    command = "mysql -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " -e 'show databases;'"

    # output bash to python variable
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    output = out.decode(encoding='utf-8')

    output_db_list_raw = output.split("\n")
    output_db_list = list(filter(None, output_db_list_raw))

    unwanted_values = ['Database']
    databases_name = [x for x in output_db_list if x not in unwanted_values]

    return databases_name


def get_list_own_db() -> list:
    """
    Retourne la liste des base de données MySQL sans celles par défaut
    """
    full_list_db = get_list_database_names()
    unwanted_values = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
    list_db = [x for x in full_list_db if x not in unwanted_values]

    return list_db


def print_list_db(list_db) -> None:
    print("\n\tListe de vos bases de données : \n")
    print('\t - %s' % '\n\t - '.join(map(str, list_db)))
    print("\n")


def print_versions_db(db_versions_array) -> None:
    print("The available versions for this db are :\n")
    for index in range(len(db_versions_array)):
        print('\t' + str(index) + " - " + db_versions_array[index] + '\t' + " saved at " + timestamp_to_date((db_versions_array[index])[0:14]))

    #print('\t - %s' % '\n\t - '.join(map(str, db_versions_array)))
    #print("\n")


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




def save_db(database_name) -> None:
    """
    Sauvegarde de la base de données passée en paramètre
    """
    current_date = get_date()
    file_name = str(BACKUP_FOLDER) + str(current_date) + "-dump_" + database_name + ".sql"
    os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + database_name + " > " + file_name)

    print("base " + database_name + " saved in folder " + BACKUP_FOLDER)


def save_all_db() -> None:
    """
    Sauvegarde de toutes les bases de données
    """
    command = ['mysqldump', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, '--all-databases', '--events']

    current_date = get_date()
    file_name = str(BACKUP_FOLDER) + current_date + "-dump_all_db.sql"

    touch(file_name)
    f = open(file_name, "w")

    return_code = subprocess.call(command, stdout=f)

    if return_code == 0:
        print("Save succesfully stored in " + str(BACKUP_FOLDER))
    else:
        sys.stderr.write("Error Code : " + str(return_code))
        sys.exit(1)

        # mysqldump -u root -perty --all-databases --events > filetest.sql


def restore_db(db_name, db_version) -> None:
    """
    Restauration de la base de données passée en paramètre
    """
    #os.system("mysql -u root -p " + database_name + " < dump_appli_web_01.sql")
    command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, db_name]

    backup_file = open(BACKUP_FOLDER+db_version)
    process = subprocess.Popen(command, stdin=backup_file)
    #print(BACKUP_FOLDER+db_version)
    process.wait()


# PENDING GUIGUI
def restore_all_db(file_name) -> None:
    """
    Restauration de toutes les bases de données
        - Regarder dans le dossier des sauvegardes si il y a des sauvegardes concernant
        l'ensemble des base de données,
        - si c'est le cas, proposer laquelle restaurer
        - si ce n'est pas le cas, proposer de rentrer le chemin du fichier manuellement
    """

    command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD]

    f = open(file_name, 'r')
    return_code = subprocess.call(command, stdin=f)

    pass


def choose_db() -> str:
    db_list = get_list_own_db()

    while True:

        print("Voici la liste de vos bases de donnees : \n")

        print_choice_db(db_list)

        db_choice = input("\nEntrez le numero correspondant a la base que vous souhaitez sauvegarder :\n")

        if db_choice.isdigit():
            db_choice = int(db_choice)
            if 0 <= db_choice < len(db_list):
                break
            else:
                print("Invalid index")
        else:
            print("Invalid index, please enter a valid index")

    db_chosen = str(db_list[db_choice])
    print("Vous avez selectionne la base : " + db_chosen)
    return db_chosen



def choose_version(array_all_versions_db) -> str:

    while True:
        print_choice_db(array_all_versions_db)
        version_choice = input("\n Please select enter the number matching the database you want to restore : \n")

        if version_choice.isdigit():
            version_choice = int(version_choice)
            if 0 <= version_choice < len(array_all_versions_db):
                break
            else:
                print("Invalid index")
        else:
            print("Invalid index, please enter a valid index")

    version_chosen = str(array_all_versions_db[version_choice])
    print("Vous avez selectionne la version : " + version_chosen)
    return version_chosen


def get_list_db_versions(db_chosen):
    # define the ls command
    ls = subprocess.Popen(["ls", "-p", BACKUP_FOLDER],
                          stdout=subprocess.PIPE,
                          )

    # define the grep command
    grep = subprocess.Popen(["grep", db_chosen],
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
    array_all_versions_db_raw = str_all_versions_db.split('\n')
    array_all_versions_db = list(filter(None, array_all_versions_db_raw))

    return array_all_versions_db







# def save_db_zip() -> None:
# 	# Sauvegarde de la db compressé :
# 	os.system('mysqldump -u appli_web -p appli_web | gzip -9 > dump_appli_web_01.sql.gz')

# def restore_db_from_zip() -> None:
# 	# Restauration de la db avec fichier compressé :
# 	os.system('gunzip < dump_appli_web_01.sql.gz | mysql -u appli_web -p appli_web')

def process_user_choice(user_choice) -> None:
    clear_screen()

    # Liste
    if user_choice == 1:

        list_db = get_list_own_db()
        print_list_db(list_db)

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

    # BENJI
    # Sauvegarde Unique
    elif user_choice == 4:

        print("Sauvegarde d'une seule base de donnees \n")
        db_chosen = choose_db()
        save_db(db_chosen)

    # Restauration Unique
    elif user_choice == 5:
        """
        - Regarder dans le dossier des sauvegardes si il y a des sauvegardes concernant 
        la db voulu
        - si c'est le cas, proposer laquelle restaurer
        - si ce n'est pas le cas, proposer de rentrer le chemin du fichier manuellement
        """

        db_chosen = choose_db()
        array_all_versions_db = get_list_db_versions(db_chosen)
        version_chosen = choose_version(array_all_versions_db)
        restore_db(db_chosen, version_chosen)


    else:
        sys.stderr.write("Error : Undefined choice\n")
        sys.exit(1)







'''
 ==== MAIN ====
'''


def main():
    clear_screen()

    print("\nBienvenue dans l'utilitaire de gestion de base de donnees.\n")
    print("\tEntrez un nombre correspondant a une action a effectuer :\n")

    print("\t[1] => Liste de vos bases de donnees.")
    print("\t[2] => Sauvegarder l'ensemble de vos base de donnees.")
    print("\t[3] => Restaurer l'ensemble de vos bases de donnees.")
    print("\t[4] => Sauvegarder une base de donnees unique.")
    print("\t[5] => Restaurer une base de donnees unique.")
    print("\t[6] => Exit.\n")

    try:
        user_choice = int(input("Votre choix ?\n> "))
    except ValueError:
        sys.stderr.write("Error : Undefined choice\n")
        sys.exit(1)

    process_user_choice(user_choice)


main()


def test():
    command = ['mysqldump', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, 'appli_web']
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

# test()
