#!/bin/bash

#
# Matt Eaton agnosticdev@gmail.com
#
# This script downloads and setups up your basic Symfony 3 Environment
# This script assumes you are running a CentOS 7 >
# This script also assumes that you are running as root
# ** Note, this server uses Systemd **
#

# Add the Webtatic Repo's to the server
echo "*** Adding the Web Tatic Repo ***"
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm

# Update the server
echo "*** Updating the Server ***"
yum update

# Install Apache 
echo "*** Installing Apache ***"
yum install httpd -y

# Start Apache
echo "*** Starting Apache ***"
systemctl start httpd

# Enable Apache at Boot
echo "*** Enabling Apache to Start on Boot ***"
systemctl enable httpd.service

# Install PHP 7
echo "*** Installing PHP7 From Webtatic ***"
yum install php70w php70w-common php70w-cli php70w-bcmath php70w-devel php70w-gd php70w-mbstring php70w-mysql php70w-pear php70w-xml -y

# Install MariaDB
echo "*** Installing MariaDB ***"
yum install mariadb-server mariadb -y

# Start MariaDB Service
echo "*** Starting MariaDB ***"
systemctl start mariadb
systemctl status mariadb

# Enable MariaDB at Boot
echo "*** Enabling MariaDB to Start on Boot ***"
systemctl enable mariadb.service

# Run the MySQL Secure Installation Script
echo "*** Running MySQL Secure Installation Script, Set Root Password!!!! ***"
mysql_secure_installation

# Inatall cURL if it is not installed
echo "*** Installing cURL if not already installed ***"
yum install curl -y

# Ask the user if they are updating or adding a user
echo -e "What would you like your Symfony project to be called?  \c"
read PROJECT

# Navigate out to the Apache exposed directory
echo "*** Navigating to where we want our Symfony site ***"
cd /var/www/html

# Download the Symfony Installer
echo "*** Downloading the Symfony Installer ***"
curl -LsS https://symfony.com/installer -o /usr/local/bin/symfony
chmod a+x /usr/local/bin/symfony

# Create a new Symfony Project
echo "*** Creating a New Symfony Project ***"
symfony new ${PROJECT}

# Install Composer Globally
echo "*** Install Composer Globally ***"
yum install wget -y
wget https://getcomposer.org/installer
php installer
mv composer.phar /usr/local/bin/composer
composer -v
