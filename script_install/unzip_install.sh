#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_unzip(){
	if [ $(is_installed /usr/bin/unzip) -eq 1 ] ; then
		echo "Installing Unzip, Please wait..."
		
		sudo apt-get install unzip -y > /dev/null 2>&1

        	echo "Install Unzip : Done"
	else
		echo "Unzip already installed";
	fi
}



install_unzip







