#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_apache(){
	if [ $(is_installed /usr/sbin/apache2) -eq 1 ] ; then
        # echo "sudo apt-get install apache2 -y"
		sudo apt-get install apache2 -y

		# Ajouter l'utilisateur au groupe apache
		sudo usermod -g www-data $USER
		# Editer les permissions pour le dossier des sites
		sudo chown -R $USER:www-data /var/www

		sudo service apache2 stop
		sudo service apache2 start

	else
		echo "apache2 already installed";
	fi
}



install_apache







