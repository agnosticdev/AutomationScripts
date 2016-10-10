#!/bin/bash
# (x86_64-apple-darwin15)
# Bash 3.0> 
#
# Bash Script Specifically Designed to Test iOS Projects
# Author: agnosticdev
# Date: 8-18-2016
#
#
# Sample command: 
# xcodebuild test -workspace /my/proj/dir/MyApp.xcworkspace -scheme MyApp
# -destination 'platform=iOS Simulator,name=iPad Pro,OS=9.3'
# -destination 'platform=iOS Simulator,name=iPad Retina,OS=9.3'
#
#

PROJECT_EXTENSION="xcodeproj"
DESTINATIONS=""

# Welcome message
echo "Hello! Let's run some automated tests!"

# Get the project directory
echo "The first thing I would like to do is get some information about your project."
echo "What is the directory path to your xcodeproj or xcworkspace project?"
echo -e "If you are in the same directory, just press enter"
read PROJECT_DIR

# Validate the porject directory
if [ "${PROJECT_DIR}" != "" ] && [ ! -d "${PROJECT_DIR}" ] ; then
	echo "The directory that your entered, '${PROJECT_DIR}' is not a valid directory"
	echo "Exiting now..."
	exit
elif [ "${PROJECT_DIR}" != "" ] ; then
	PROJECT_DIR="${PROJECT_DIR}/"
fi


# Ask if their project is a xcworkspace or a xcodeproj
echo "Is your project a xcworkspace?"
echo -e "[y/n] "
read EXTENSION

# Attempt to validate response
if [ "${EXTENSION}" != "n" ] && [ "${EXTENSION}" != "y" ] ; then
	echo "You did not provide a valid answer"
	echo "Exiting now..."
	exit
else
	if [ "${EXTENSION}" == "y" ] ; then
		PROJECT_EXTENSION="xcworkspace"
	fi
fi 

# Ask for the name of the project
echo -e "What is your project name?"
read PROJECT_NAME

if [ "${PROJECT_NAME}" == "" ] ; then
	echo "You did not provide a valid project name"
	echo "Exiting now..."
	exit	
fi

# Ask for the scheme
echo -e "What is the scheme of your project?"
read SCHEME

if [ "${SCHEME}" == "" ] ; then
	echo "You did not provide a valid scheme name"
	echo "Exiting now..."
	exit	
fi

# Gather destinations
echo "Destination format: platform=Simulator,name=iPhone,OS=8.1"
echo -e "Please enter a destination: "
while read DEST
do

    DESTINATIONS="${DESTINATIONS} -destination '${DEST}'"
    echo -e "Are you finished ? [y/n]"
    read FINISHED

    if [ "${FINISHED}" == "y" ] ; then
    	break
    else 
    	echo "Please enter another destination: "
    fi
done

echo "DEST: ${DESTINATIONS}"

# Build the list of parameters for the test
if [ "${PROJECT_EXTENSION}" == "xcworkspace" ] ; then
	COMMANDS="xcodebuild test -workspace ${PROJECT_DIR}${PROJECT_NAME}.${PROJECT_EXTENSION} -scheme ${SCHEME} ${DESTINATIONS}"
else
	COMMANDS="xcodebuild test -project ${PROJECT_DIR}${PROJECT_NAME}.${PROJECT_EXTENSION} -scheme ${SCHEME} ${DESTINATIONS}"
fi

echo "Commands: ${COMMANDS}"

echo "------------------------------------------------------------"
echo "OK, executing tests!"
echo ""
eval $COMMANDS

if [ $? -eq 0 ]; then
    echo "SUCCESS, now parse the output!!!"
else
    echo "Failure, please checkout what went wrong"
fi

# TODO
# ----------------------------
# Gather results
# Write the results to a log file or report them somewhere
#
