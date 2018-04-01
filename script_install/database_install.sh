echo "Déploiement de la BDD..."
echo "Veuillez entrer le mot de passe root MySQL : "

mysql -u root -p -e 'source /var/www/html/appli_web/appli_web.sql'

echo "Déploiement de la BDD : Done"
