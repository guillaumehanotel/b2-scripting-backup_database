#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_mysql(){

	if [ $(is_installed /usr/bin/mysql) -eq 1 ] ; then
        echo "Installing MySQL, Please wait..."
		sudo apt-get -y install mysql-server
       	        echo "Installing MySQL : Done"
	else
		echo "MySQL already installed";
	fi
}



install_mysql

