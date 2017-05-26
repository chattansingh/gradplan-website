#!/bin/bash
#importing backup database and restoring last backup of website
apt-get -y update &> /dev/null 2>&1;
apt-get -y upgrade &> /dev/null 2>&1;
apt-get -y install apache2 &> /dev/null 2>&1;
apt-get -y install postgresql postgresql-contrib 2>&1;
#note this is not fully secure
cd ~/backup

tar -zxpvf websitebackup.tar.gz &> /dev/null 2>&1;
mv gradplanproject ~/;
chown :www-data ~/gradplanproject;
chown :www-data -R ~/gradplanproject;

su postgres;
psql -f database.bak postgres
