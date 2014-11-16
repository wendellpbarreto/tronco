#!/bin/bash
#
#-----------------------------------
# @autor: Wendell P. Barreto
# @email: wendellp.barreto@gmail.com
# @project: tronco
# @doc: restart_db.sh
# ----------------------------------


while true; do
    read -p "Are you using Linux (y or n)? " yn
    case $yn in
        [Yy]* )
        	sudo -u postgres psql -c 'DROP DATABASE tronco_db'
			sudo -u postgres psql -c 'CREATE DATABASE tronco_db'
			sudo -u postgres psql -c 'CREATE USER tronco_admin'
			sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE tronco_db TO tronco_admin'
			sudo -u postgres psql -d tronco_db -c 'CREATE EXTENSION hstore'

			break;;
        [Nn]* )
			psql -c 'DROP DATABASE tronco_db'
			psql -c 'CREATE DATABASE tronco_db'
			psql -c 'CREATE USER tronco_admin'
			psql -c 'GRANT ALL PRIVILEGES ON DATABASE tronco_db TO tronco_admin'
			psql -d tronco_db -c 'CREATE EXTENSION hstore'

			break;;
        * ) echo "Please answer yes or no.";;
    esac
done

python manage.py syncdb
python manage.py collectstatic --noinput