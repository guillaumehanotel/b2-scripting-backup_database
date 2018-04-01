echo "Installing webste, Please wait..."

if [ -f /var/www/html/index.html ]; then
	# Suppression default apache page
	sudo rm /var/www/html/index.html > /dev/null 2>&1
fi



if [ ! -d /var/www/html/appli_web/ ]; then
	# Import du site web
	git clone https://github.com/guillaumehanotel/appli_web $HOME/appli_web/ > /dev/null 2>&1

	# Déplacement du site dans le serveur
	sudo mv $HOME/appli_web/ /var/www/html > /dev/null 2>&1

	# Mettre l'utilisateur dans le groupe www-data
	sudo usermod -g www-data $USER > /dev/null 2>&1

	# Change user & group of website
	sudo chown -R www-data:www-data /var/www/html/appli_web/ > /dev/null 2>&1
fi



if [ ! -f /etc/apache2/sites-available/001-appli_web.conf ]; then

	# Création d'un nouveau virtual Host
	sudo cp $HOME/postgreSQL/script_install/001-appli_web.conf /etc/apache2/sites-available/ > /dev/null 2>&1

	# Activation du virtual host
	sudo a2ensite 001-appli_web > /dev/null 2>&1

	# Rechargement d'apache
	sudo service apache2 reload > /dev/null 2>&1

	# Activation du module Apache rewrite qui permet l'utilisation des fichiers .htaccess
	sudo a2enmod rewrite > /dev/null 2>&1

	# Redémarrage d'apache
	sudo service apache2 restart > /dev/null 2>&1

	# Désactivation du virtual host par défaut
	sudo a2dissite 000-default > /dev/null 2>&1

	# Modification de la configuration général d'apache 
	# Suppression de la directive Indexes pour le dossier /var/www (permet de lister les fichiers si il ny a pas dindex)

	sudo sed -i -e 's/Options Indexes FollowSymLinks/Options FollowSymLinks/' /etc/apache2/apache2.conf > /dev/null 2>&1

	# Rechargement d'apache
	sudo service apache2 reload > /dev/null 2>&1

fi




