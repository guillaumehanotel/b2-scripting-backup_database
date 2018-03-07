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
import colors

# Databases are stored in : /var/lib/mysql

# TODO : reformat restore_all_db()
# TODO : proposer la sauvegarde distante (ssh)

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


def alter_db():
    os.system("mysql -u root -perty appli_web -e 'UPDATE user SET user_pseudo = \"satan\" WHERE user_id = 1'")


def select_user():
    os.system("mysql -u root -perty appli_web -e 'SELECT * from user'")


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


def get_list_db_names() -> list:
    """
    Retourne la liste des base de données MySQL
    """

    command = "mysql -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " -e 'show databases;'"

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
    colors.print_cyan("\n\tYour databases are: \n")
    print('\t - %s' % '\n\t - '.join(map(str, list_db)))
    print("\n")


def print_versions_db(db_versions_array) -> None:
    print("The available versions for this db are :\n")
    for index in range(len(db_versions_array)):
        print('\t' + str(index) + " - " + db_versions_array[index] + '\t' + " saved at " + timestamp_to_date((db_versions_array[index])[0:14]))


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
    current_date = get_date()
    file_name = str(BACKUP_FOLDER) + str(current_date) + "-dump_" + db_name + ".sql"
    os.system("mysqldump -u " + MYSQL_USER + " -p" + MYSQL_PASSWORD + " " + db_name + " > " + file_name)

    print(colors.GREEN + "\nDatabase " + colors.ESCAPE + "\""+db_name + "\"" + colors.GREEN + " successfully saved in folder "+ colors.ESCAPE + colors.YELLOW + BACKUP_FOLDER + colors.ESCAPE)


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
    
    clear_screen()
    colors.print_cyan("Saving all your databases...\n")

    if return_code == 0:
        print(colors.GREEN + "Databases successfully saved in: " + colors.YELLOW +str(BACKUP_FOLDER) + colors.ESCAPE)
        print(" ")
    else:
        sys.stderr.write("Error Code : " + str(return_code))
        sys.exit(1)


def restore_db(db_name, db_version) -> None:
    """
    Restauration de la base de données passée en paramètre
    """
    command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD, db_name]

    backup_file = open(BACKUP_FOLDER+db_version)
    process = subprocess.Popen(command, stdin=backup_file)
    process.wait()


# TODO color this function
def restore_all_db(db_version) -> None:

    command = ['mysql', '-u', MYSQL_USER, '-p' + MYSQL_PASSWORD]

    backup_file = open(BACKUP_FOLDER+db_version, 'r')
    process = subprocess.Popen(command, stdin=backup_file)
    process.wait()



def choose_db() -> str:
    db_list = get_list_own_db()

    while True:

        colors.print_cyan("Your databases are : \n")

        print_choice_db(db_list)

        db_choice = input(colors.CYAN +"\nEnter the number matching the database your want to save:"+ colors.ESCAPE +"\n> ")

        if db_choice.isdigit():
            db_choice = int(db_choice)
            if 0 <= db_choice < len(db_list):
                break
            else:
                print("Invalid index")
        else:
            print("Invalid index, please enter a valid index")

    db_chosen = str(db_list[db_choice])
    print("\nYou selected database : " + colors.YELLOW + db_chosen + colors.ESCAPE)
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






def process_user_choice(user_choice) -> None:
    clear_screen()

    # Liste
    if user_choice == 1:

        list_db = get_list_own_db()
        print_list_db(list_db)

    # Sauvegarde All
    elif user_choice == 2:
        save_all_db()

    # Restauration All
    elif user_choice == 3:
        ls = subprocess.Popen(["ls", "-p", BACKUP_FOLDER],
                              stdout=subprocess.PIPE,
                              )

        # define the grep command
        # TODO set global variable name for "dump_all_db"
        grep = subprocess.Popen(["grep", "dump_all_db"],
                                stdin=ls.stdout,
                                stdout=subprocess.PIPE,
                                )

        # read from the end of the pipe (stdout)
        endOfPipe = grep.stdout

        str_all_global_backups = ""

        for line in endOfPipe:
            str_all_global_backups = str_all_global_backups + line.decode('utf-8')


        if str_all_global_backups == "":
            print("No global backup found. Please make one already !!")
        else:
            array_all_versions_db_raw = str_all_global_backups.split('\n')
            array_all_versions_db = list(filter(None, array_all_versions_db_raw))

            version_chosen = choose_version(array_all_versions_db)
            restore_all_db(version_chosen)

    # Sauvegarde Unique
    elif user_choice == 4:

        colors.print_cyan("Save a single database :\n")
        db_chosen = choose_db()
        save_db(db_chosen)


    # Restauration Unique
    elif user_choice == 5:

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
    clear_screen()

    print("\nWelcome to the database management program.\n")
    colors.print_cyan("Please enter a number matching your choice :\n")

    print("\t[1] =>" + colors.CYAN + " List" + colors.ESCAPE +" your databases.")
    print("\n\t[2] =>" + colors.CYAN +" Save all" + colors.ESCAPE +" your databases.")
    print("\t[3] =>" + colors.CYAN + " Restore all"+ colors.ESCAPE + " your databases.")

    print("\n\t[4] =>" + colors.CYAN +  " Save a single" + colors.ESCAPE + " database.")
    print("\t[5] =>" + colors.CYAN +  " Restore a single" + colors.ESCAPE + " database.")

    print("\n\t[6] => Exit.\n")


    try:
        user_choice = int(input("Enter your choice:\n> "))
    except ValueError:
        sys.stderr.write("Error : Undefined choice\n")
        sys.exit(1)

    process_user_choice(user_choice)


main()


