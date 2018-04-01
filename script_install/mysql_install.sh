#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_mysql(){

	if [ $(is_installed /usr/bin/mysql) -eq 1 ] ; then
        echo "Installing MySQL..."
		sudo apt-get -y install mysql-server
        echo "Done"
	else
		echo "mysql already installed";
	fi
}



install_mysql

