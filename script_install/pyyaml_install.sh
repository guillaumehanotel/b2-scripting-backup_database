tar zxvf ../PyYAML-3.12.tar.gz > /dev/null 2>&1
sudo chown -R $USER /usr/local/lib/python3.4
cd $HOME/postgreSQL/script_install/PyYAML-3.12 
python3 setup.py install > /dev/null 2>&1
