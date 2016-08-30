#!/bin/bash
#

# Make sure the files exist before we attempt to run the script
if [ ! -f "latency_test.py" ]; then
	echo "Could not find your Python script???"
	echo "Exiting..."
fi

# Set file permissions on the file we are about to run
chmod 775 latency_test.py

# Execute the python script
python latency_test.py