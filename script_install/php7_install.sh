#!/bin/bash

is_installed(){
    command -v $1 >/dev/null 2>&1
    echo $?
}

install_php7(){

	if [ $(is_installed /usr/bin/php7.1) -eq 1 ] ; then
        echo "Installing PHP7.1..."

		sudo apt-get install apt-transport-https lsb-release ca-certificates

		sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg

		sudo echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list

		sudo apt-get update

		sudo apt install --no-install-recommends php7.1 libapache2-mod-php7.1 php7.1-mysql php7.1-curl php7.1-json php7.1-gd php7.1-mcrypt php7.1-msgpack php7.1-memcached php7.1-intl php7.1-sqlite3 php7.1-gmp php7.1-geoip php7.1-mbstring php7.1-redis php7.1-xml php7.1-zip

        echo "Done"

	else
		echo "php7 already installed";
	fi
}



install_php7







