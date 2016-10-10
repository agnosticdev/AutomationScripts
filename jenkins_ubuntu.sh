#!/bin/bash

#
# Matt Eaton agnosticdev@gmail.com
#
# This script downloads a Jenkins CI
# This script assumes you are running a Ubuntu 14.04 > server
# This script also assumes that you are running as root
# Note, Jenkins is using init.d
#

# Install Python Software Properties
# This allows you to manage where you get packages from
echo "*** Installing Python Software Properties ***"
apt-get install python-software-properties -y

# Notify the package list about Jenkins
wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'

# Download the package list from the repos
echo "*** Updating the existing package list ***"
apt-get update

# Attempt to install Jenkins
apt-get install jenkins

# Attempt to install Apache2
# Also attempt to enable the proxy and proxy_http modules so that a proxy can route traffic
# from 80 to 8080 and a URL can be applied to the Jenkins setup
echo "*** Installing Apache ***"
apt-get install apache2 -y
echo "*** Enabling proxy and proxy_http modules ***"
a2enmod proxy
a2enmod proxy_http

# Creating a virtual host so Apache can route traffic to Jenkins
echo "*** Creating a virtual host for Jenkins.  Hit Enter ***"
cat <<EOF >/etc/apache2/sites-available/jenkins.conf
<VirtualHost *:80> 
  ServerAdmin webmaster@localhost
  ServerName jenkins.url.com
  ServerAlias jenkins
  ProxyRequests Off
  <Proxy *>
    Order deny,allow
    Allow from all
  </Proxy>
  ProxyPreserveHost on
  ProxyPass / http://localhost:8080/ nocanon
  AllowEncodedSlashes NoDecode
</VirtualHost>
EOF

# Enabling the new Jenkins site for the config file we just created
echo "*** Enabling the Jenkins site! ***"
a2ensite jenkins

# Restarting Apache
echo "*** Restarting Apache so modules can be recognized ***"
service apache2 reload
echo "*** Checking the status of Apache ***"
service apache2 status

# Enable port forwarding between 80 and 8080
# Information found at: https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu
# Requests from outside
echo "*** Enabling Port Forwarding ***"
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
#Requests from localhost
iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 80 -j REDIRECT --to-ports 8080

# Update the existing packages
echo "*** Upgrading the existing packages ***"
apt-get upgrade -y

# Reboot Server
echo "*** Rebooting Server. Bye! ***"
reboot
