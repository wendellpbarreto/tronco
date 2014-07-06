#!/bin/bash
#
#-----------------------------------
# @autor: Wendell P. Barreto
# @email: wendellp.barreto@gmail.com
# @project: mcc
# @doc: restart_db.sh
# ----------------------------------


while true; do
    read -p "Are you using Linux (y or n)? " yn
    case $yn in
        [Yy]* )
        	sudo -u postgres psql -c 'DROP DATABASE mcc_db'
			sudo -u postgres psql -c 'CREATE DATABASE mcc_db'
			sudo -u postgres psql -c 'CREATE USER mcc_admin'
			sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE mcc_db TO mcc_admin'
			# sudo -u postgres psql -d mcc_db -c 'CREATE EXTENSION hstore'

			break;;
        [Nn]* )
			psql -c 'DROP DATABASE mcc_db'
			psql -c 'CREATE DATABASE mcc_db'
			psql -c 'CREATE USER mcc_admin'
			psql -c 'GRANT ALL PRIVILEGES ON DATABASE mcc_db TO mcc_admin'
			# psql -d mcc_db -c 'CREATE EXTENSION hstore'

			break;;
        * ) echo "Please answer yes or no.";;
    esac
done

python manage.py syncdb
python manage.py collectstatic --noinput