#!/bin/bash
#

# Make sure the files exist before we attempt to run the script
if [ ! -f "drupal_local.ini" ]; then
	echo "Could not find you configuation file?"
	echo "Exiting..."
fi

if [ ! -f "drupal_local.py" ]; then
	echo "Could not find your Python script???"
	echo "Exiting..."
fi

# Set file permissions on the file we are about to run
chmod 775 drupal_local.py

# Execute the python script
python drupal_local.py