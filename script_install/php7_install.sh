#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_php7(){

	if [ $(is_installed /usr/bin/php7.1) -eq 1 ] ; then
        echo "Installing PHP 7.1, Please Wait..."

		sudo apt-get install apt-transport-https lsb-release ca-certificates -y > /dev/null 2>&1

		sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg > /dev/null 2>&1

		echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list > /dev/null 2>&1

		sudo apt-get update > /dev/null 2>&1

		sudo apt install --no-install-recommends php7.1 libapache2-mod-php7.1 php7.1-mysql php7.1-curl php7.1-json php7.1-gd php7.1-mcrypt php7.1-msgpack php7.1-memcached php7.1-intl php7.1-sqlite3 php7.1-gmp php7.1-geoip php7.1-mbstring php7.1-redis php7.1-xml php7.1-zip -y > /dev/null 2>&1

        echo "Installing PHP 7.1 : Done"

	else
		echo "PHP 7.1 already installed";
	fi
}



install_php7







