# AutomationScripts
This is a collection of automation scripts that can be used for various use cases throughout development.

## Drupal Local
The purpose of this script is to eliminate the need to manually back up your database and files directory in a drupal site.  Often, in times of debugging, it is handy to setup a testing site to test different scenarios in Drupal and this the drupal_local.sh script can help with the database and file operations needed to setup your testing scenario.

## Latency Test
The purpose of this script is to perform very very simple latency testing against an anonymous endpoint.  When I say anonymous, I mean a non-authenticated request against a URL.
Currently, the script only performs GET requests.
The script will accumulate the total amount of time needed to execute the request and average it all together to display an average latency when all requests are finished.
