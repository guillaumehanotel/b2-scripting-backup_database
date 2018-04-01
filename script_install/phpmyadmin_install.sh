#!/bin/bash

is_installed(){
    dpkg --list | grep $1 >/dev/null 2>&1
    echo $?
}

install_phpmyadmin(){

	if [ $(is_installed phpmyadmin) -eq 1 ] ; then
        echo "Installing PHPMyAdmin, Please Wait..."

	sudo apt-get install phpmyadmin -y

        echo "Installing PHPMyAdmin : Done"

	else
		echo "PHPMyAdmin already installed";
	fi
}



install_phpmyadmin







