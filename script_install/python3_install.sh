#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_php7(){

	if [ $(is_installed /usr/bin/python3.4) -eq 1 ] ; then
        echo "Installing Python 3, Please Wait..."

	sudo apt-get install python3 -y > /dev/null 2>&1

        echo "Installing Python 3 : Done"

	else
		echo "Python 3 already installed";
	fi
}



install_php7







