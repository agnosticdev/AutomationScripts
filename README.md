# AutomationScripts
This is a collection of automation scripts that can be used for various use cases throughout development.

## Drupal Local
The purpose of this script is to eliminate the need to manually back up your database and files directory in a drupal site.  Often, in times of debugging, it is handy to setup a testing site to test different scenarios in Drupal and this the drupal_local.sh script can help with the database and file operations needed to setup your testing scenario.

## Latency Test
The purpose of this script is to perform very very simple latency testing against an anonymous endpoint.  When I say anonymous, I mean a non-authenticated request against a URL.
Currently, the script only performs GET requests.
The script will accumulate the total amount of time needed to execute the request and average it all together to display an average latency when all requests are finished.

## Jenkins_Install_Script
The following script is a bash script that should help you get Jenkins up and running on a Ubuntu 14.04 server fast easily

## Symfony_Install_Script
CentOS Bash Script to setup a server and install Symfony

## iOSTestAutomation
Bash script to gather information from a user about automated tests that they want to run on a project.
The script then runs the tests on each of the destinations, compiles the results and writes them to a log.
