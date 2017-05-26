#!/bin/bash
#NOTE THIS IS ASSUMING YOU ARE RUNNING AS ROOT
#THIS SCRIPT SECURES APACHE2 INSTALL AND REDIRECTS ALL TRAFFIC TO HTTPS://
#update repositories first
#assumes running in as gradplan user
printf "Updating and upgrading...\n"
apt-get -y update &> /dev/null 2>&1;
apt-get -y upgrade &> /dev/null 2>&1;


printf "Securing and modifying Apache configuration...\n"
#enable ssl apache2 support module
( (
printf "Enabling Apache SSL module...\n"
a2enmod ssl;
#restart the service to recognize the change
printf "Restarting Apache server...\n"
service apache2 restart;
#make directory to place certs
printf "Removing old certificates..\n"
rm -R /etc/apache2/ssl
printf "Creating SSL Directory...\n"
mkdir -p /etc/apache2/ssl;
#create both key and certificate for the website
printf "Generating self signed certificate and RSA key...\n"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt <<< $'US\nCalifornia\nLos Angeles\n424Sec\nCyber\n192.168.1.120\n\n' &> /dev/null 2>&1;
#create a backup for conf files before we overwrite them
printf "Backing up default configuration files...\n"
cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf.bak;
cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.com.bak;
cp /etc/apache2/conf-enabled/security.conf /etc/apache2/conf-enabled/security.conf.bak
cp /etc/apache2/mods-enabled/dir.conf /etc/apache2/mods-enabled/dir.conf.bak
#next two printf change the conf files to setup ssl
#the ip variable will hold the servers current ip address to make sure it's correctly assigned
ip="$(ifconfig | grep -m 1 "inet " | awk -F'[: ]+' '{ print $4 }')"
#modifies the conf to auto redirect any http to https
printf "Setting up HTTP redirect to HTTPS...\n"
printf "
<VirtualHost *:80>
        ServerAdmin ervsec@gmail.com
        DocumentRoot /var/www/html
        #Server's IP %s
        ServerName %s
        #Redirect all http to https
        RewriteEngine On
        RewriteCond %%{SERVER_PORT} !^443$
        RewriteRule ^(.*)$ https://%%{HTTP_HOST}\$1 [R=301,L]
</VirtualHost>" $ip $ip > /etc/apache2/sites-available/000-default.conf;
#secure the server using the proper SSL configuration
#SSLCompression off > Defends against CRIME Attack
#SSLProtocol ... > Defends against SSL downgrade / POODLE
#SSLCipherSuite > cipher suites that provide Perfect Forward Secrecy
printf "Configuring SSL...\n"
printf "
<IfModule mod_ssl.c>
    <VirtualHost _default_:443>
        ServerAdmin ervsec@gmail.com
        ServerName gradplan.com
        ServerAlias www.gradplan.com
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        SSLEngine on
        SSLCompression off
        SSLProtocol All -SSlv2 -SSLv3 -TLSv1
        SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
        SSLCertificateFile /etc/apache2/ssl/apache.crt
        SSLCertificateKeyFile /etc/apache2/ssl/apache.key
                
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        #Stat digital ocean setup
        Alias /static /home/gradplan/gradplanproject/static
        <Directory /home/gradplan/gradplanproject/static>
            Require all granted
        </Directory>
        
        <Directory /home/gradplan/gradplanproject/gradplanproject>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

        WSGIDaemonProcess gradplanproject python-path=/home/gradplan/gradplanproject python-home=/home/gradplan/gradplanproject/gradplanprojectenv
        WSGIProcessGroup gradplanproject
        WSGIScriptAlias / /home/gradplan/gradplanproject/gradplanproject/wsgi.py
        WSGIApplicationGroup %%{GLOBAL}  
        #End Digital ocean setup 

        BrowserMatch \"MSIE [2-6]\" \\
        nokeepalive ssl-unclean-shutdown \\
        downgrade-1.0 force-response-1.0
        BrowserMatch \"MSIE [17-9]\" ssl-unclean-shutdown
    </VirtualHost>
</IfModule>
" > /etc/apache2/sites-available/default-ssl.conf;
#remove server information so attacker cannot gain extra info
printf "Putting server into production mode...\n"
printf "
ServerTokens Prod
ServerSignature Off
TraceEnable Off
" > /etc/apache2/conf-enabled/security.conf
#tell apache to look at .php files first before any other extension
printf "Configuring directory settings...\n"
printf "
<IfModule mod_dir.c>
        DirectoryIndex index.html index.cgi index.pl index.php  index.xhtml index.htm
</IfModule>
" > /etc/apache2/mods-enabled/dir.conf
#remove the apache2 default index.html it is not needed
printf "Removing default index.html...\n"
rm /var/www/html/index.html
#enable the ssl virtual host for ssl connection
printf "Enabling SSL configuration...\n"
a2ensite default-ssl.conf;
#restart the apache server to recognize the changes
printf "Enabling Rewrite Mod...\n"
a2enmod rewrite
printf "Check Apache2 Syntax for Errors...\n"
apache2ctl configtest
printf "Restarting Apache...\n"
service apache2 restart;
printf "Apache ready..\nHave a nice day.\n"
) &)
