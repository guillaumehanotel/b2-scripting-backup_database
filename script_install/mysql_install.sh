#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_mysql(){

	if [ $(is_installed /usr/bin/mysql) -eq 1 ] ; then

		export DEBIAN_FRONTEND="noninteractive"
		sudo debconf-set-selections <<< "mysql-server mysql-server/root_password erty $1"
		sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again erty $1"
		sudo apt-get -y install mysql-server

	else
		echo "mysql already installed";
	fi
}



install_mysql

