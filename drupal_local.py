#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The purpose of this script is to automate syncronization on Drupal projects from backups
# This script will reload file directories and rebuild local databases
# This script has not be run against remote sources but it doe not seem unreasonable to extend it in this way
# This script is entry point for the functionality an should be executed with the shell script
#
from __future__ import print_function
import ConfigParser, os, sys


############ Script Entry Point ############
# Dictionary to hold config variables
global_vars = {}

try:
	config = ConfigParser.ConfigParser()
	config.read('drupal_local.ini')
	global_vars["database_name"] = config.get("DEFAULT", "database_name")
	global_vars["database_file_location"] = config.get("DEFAULT", "database_file_location")
	global_vars["files_location"] = config.get("DEFAULT", "files_location")
	global_vars["drupal_files_location"] = config.get("DEFAULT", "drupal_files_location")
	global_vars["verbose"] = bool(config.get("DEFAULT", "verbose"))
	global_vars["mysql_user"] = config.get("DEFAULT", "mysql_user")
	global_vars["mysql_password"] = config.get("DEFAULT", "mysql_password")
	global_vars["files_username"] = config.get("DEFAULT", "files_username")
	global_vars["files_groupname"] = config.get("DEFAULT", "files_groupname")
except Exception, e:
	print("Unexpected error loading config file: " + str(e))
	raise


# Make sure all variables are filled with a valid value
for k,v in global_vars.iteritems():
	if global_vars[k] == "" or global_vars[k] is None:
		exit("Please make sure that " +str(global_vars[k]) + " is set in the config file")
	else:
		if global_vars["verbose"]:
			print(k + " => " +str(global_vars[k]))


############ Database Transactions ############

# Build database backup string command

database_backup_file = global_vars["drupal_files_location"] + global_vars["database_name"] + "_backup.sql"
mysql_backup = "mysqldump -u"+ global_vars["mysql_user"] + " -p" + global_vars["mysql_password"]
mysql_backup += " " + global_vars["database_name"] + " > " + database_backup_file

# Perform a backup of the database
if global_vars["verbose"]:
	print("*** Backing up current database in case of failure ***")
os.system(mysql_backup)

# Build drop string command
try:
	# Build deletion command
	mysql_delete = "mysqladmin -u"+ global_vars["mysql_user"] + " -p"+ global_vars["mysql_password"]
	mysql_delete += " drop " + global_vars["database_name"]

	# Execute the deletion
	if global_vars["verbose"]:
		print("*** Deleting current database ***")
	os.system(mysql_delete)

	# Build the creation command
	mysql_creation = "mysqladmin -u"+ global_vars["mysql_user"] + " -p"+ global_vars["mysql_password"]
	mysql_creation += " create " + global_vars["database_name"]
	# Execute the creation
	if global_vars["verbose"]:
		print("*** Create new database ***")
	os.system(mysql_creation)

	# Build import command
	mysql_import = "mysql -u"+ global_vars["mysql_user"] + " -p"+ global_vars["mysql_password"]
	mysql_import += " " + global_vars["database_name"] + " < " + global_vars["database_file_location"]

	# Import new database
	if global_vars["verbose"]:
		print("*** Import new data into the newly created database ***")
	os.system(mysql_import)

except Exception, e:
	print("Unexpected error running database transactions: " + str(e))
	# Build a command to restore database
	mysql_restore = "mysqldump -u"+ global_vars["mysql_user"] + " -p"+ global_vars["mysql_password"]
	mysql_restore += " " + global_vars["database_name"] + " < " + database_backup_file
	if global_vars["verbose"]:
		print("*** Something went wrong while running the database transactions ***")
	os.system(mysql_restore)
	exit("Exiting due to database transactional error")



# Let the user know that the database transactions were completed successfully
if global_vars["verbose"]:
	print("*** Database transactions completed successfully ***")

############ File Operations ############
backup_files_command = "cp -a " + global_vars["drupal_files_location"] + "/files/." 
backup_files_command += " " + global_vars["drupal_files_location"] + "/files_backup" 

# Backup files directory
if global_vars["verbose"]:
	print("*** Backing up files directory ***")
os.system(backup_files_command)

try:
	remove_file_command = "rm -rf " + global_vars["drupal_files_location"] + "/files" 

	# Remove old files directory
	if global_vars["verbose"]:
		print("*** Removing old files directory ***")
	os.system(remove_file_command)

	copy_files_command = "cp -R " + global_vars["files_location"] + " " + global_vars["drupal_files_location"] + "/files"
	# Copy new files into the drupal files directory
	if global_vars["verbose"]:
		print("*** Attempting to copy new files into existing Drupal files directory ***")
	os.system(copy_files_command)

	file_permissions_command = "sudo chmod -R 775 " + global_vars["drupal_files_location"] + "/files"
	# Set the new file permissions on the files directory
	if global_vars["verbose"]:
		print("*** Attempting to set the file permissions on the new files directory ***")
	os.system(file_permissions_command)

	file_ownership_command = "sudo chown -R " + global_vars["files_username"] + ":" + global_vars["files_groupname"]
	file_ownership_command += " " + global_vars["drupal_files_location"] + "/files"
	# Set the new file ownership on the files directory
	if global_vars["verbose"]:
		print("*** Attempting to set the file ownership on the new files directory ***")
	os.system(file_ownership_command)

except Exception, e:
	print("Unexpected error running file operations: " + str(e))
	# Build a command to restore files
	files_restore = "cp -R " + global_vars["drupal_files_location"] + "/files_backup"
	files_restore += " " + global_vars["drupal_files_location"] + "/files" 
	# Attempt to restore files
	if global_vars["verbose"]:
		print("*** Something went wrong, restoring files ***")
	os.system(files_restore)

	file_restore_permissions_command = "sudo chmod -R 775 " + global_vars["drupal_files_location"] + "/files && "
	file_restore_permissions_command += "sudo chown -R " + global_vars["files_username"] + ":" + global_vars["files_groupname"]
	file_restore_permissions_command += " " + global_vars["drupal_files_location"] + "/files"
	# Attempt to restore file permissions
	if global_vars["verbose"]:
		print("*** Restoring file ownership and permissions ***")
	os.system(file_restore_permissions_command)
	exit("Exiting due to file operation error")

# Let the user know that the file operations were completed successfully
if global_vars["verbose"]:
	print("*** File operations completed successfully ***")

if global_vars["verbose"]:
	print("*** At this point it is recommended to clear the drupal cache ***")

clear_cache = "cd " + global_vars["drupal_files_location"] + " && drush cc"
os.system(clear_cache)

# Asking about cleanup operations
cleanup = ""
if (sys.version_info > (3, 0)):
	cleanup = input("Do you wish to remove the backup files directory and database file? [y/n] ")
else:
	cleanup = raw_input("Do you wish to remove the backup files directory and database file? [y/n] ")
cleanup = cleanup.strip()

if cleanup == 'y':
	if global_vars["verbose"]:
		print("*** Cleaning up backup data ***")

	# Remove backup files
	backup_files_removal = "sudo rm -rf " + global_vars["drupal_files_location"] + "/files_backup" 
	os.system(backup_files_removal)

	# Remove backup database
	backup_database_removal = "sudo rm -rf " + database_backup_file
	os.system(backup_database_removal)

print("*** Script finished ***")
exit("Exiting successfully")