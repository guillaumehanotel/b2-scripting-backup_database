.PHONY: help install

help:
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-10s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'


server_install: ## Installe un serveur web avec un site
	./apache2_install.sh
	./php7_install.sh
	./mysql_install.sh
	./phpmyadmin_install.sh
	./website_install.sh
	./database_install.sh


script_install: ## Installe les dépendances pour le script de sauvegarde
	./python3_install.sh
	./pyyaml_install.sh
	./unzip.sh
