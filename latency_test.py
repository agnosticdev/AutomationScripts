#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The purpose of this script is to simply make anonymous GET requests to test latency
# These requests do not contain authentication or headers
# The only things that are asked from the user is the URL and the times they wish to run the URL
#
from __future__ import print_function
import os, sys, time
from datetime import datetime
try:
	import requests
except ImportError, e:
	print("Unexpected error, the requests module was not found: " + str(e))
	requests_install = ""
	# Ask the user if they wish to install requests if they do not have it installed
	if (sys.version_info > (3, 0)):
		requests_install = input("Do you wish to use pip to install requests? [y/n] ")
	else:
		requests_install = raw_input("Do you wish to use pip to install requests? [y/n] ")
	requests_install = requests_install.strip()

	# run the installation if the users wishes to install requests
	if requests_install == 'y':
		requests_command = ""
		if (sys.version_info > (3, 0)):
			requests_command = "pip3 install requests"
		else:
			requests_command = "pip install requests"
		os.system(requests_command)


print("************************** Testing Start **************************")

# *** Get URL ***
full_url = ""
if (sys.version_info > (3, 0)):
	full_url = input("What is the full url that you wish to test? ")
else:
	full_url = raw_input("What is the full url that you wish to test? ")
full_url = full_url.strip()

# Based upon http:// is 7 characters, I do not think any URL should be less than 9 characters
if len(full_url) < 9:
	print("It looks like your URL is less than 9 characters, please check this again")
	exit("Exiting now...")	

# 1 st attempt to validate the url input
if "http" not in full_url:
	print("Could not find http or https in the URL you provided")
	exit("Exiting now...")

# 2nd attempt to validate the url input
if "://" not in full_url:
	print("Could not find :// in the URL you provided")
	exit("Exiting now...")

# *** Get number of times to run URL ***

url_execution_amount = 0
if (sys.version_info > (3, 0)):
	url_execution_amount = input("How many times would you like to run this URL? ")
else:
	url_execution_amount = raw_input("How many times would you like to run this URL? ")

try:
   url_execution_amount = int(url_execution_amount)
except ValueError:
   print("Looks like the input received was not numeric? ")
   exit("Exiting now...")

# *** Execution of the URL n times ***
def execute_requests(url, execution_amount):

	n = 0
	requested_times = []
	success_codes = 0
	while n < int(execution_amount):
		start_time = time.time()
		# Perform request
		r = requests.get(url)
		elapsed_time = time.time() - start_time
		requested_times.append(elapsed_time)
		e = (n + 1)
		if r.status_code > 400:
			print("Iteration: " + str(e) + " for URL: " + url + " returned a status code of: " + str(r.status_code))
		else:
			success_codes += 1
			print("Iteration: " + str(e) + " of URL: " + url + " resulted in a page load time of: " + str(elapsed_time), " with status code: "+ str(r.status_code))
		n += 1
	average = 0
	for num in requested_times:
		average += num
	average = (average / execution_amount)

	results_string = "Requesting URL: " + url + ", " + str(execution_amount) + " times resulted in: " + str(success_codes)
	results_string += " successful requests, with an average latency of: "+ str(average)
	print(results_string)

# Execute the test as many
flag = True
while (flag):
	execute_requests(full_url, url_execution_amount)
	again = ""
	if (sys.version_info > (3, 0)):
		again = input("Do you wish to run this test again? [y/n] ")
		if not isinstance(again, str):
			exit("Did not recognize your input, exiting...")
	else:
		again = raw_input("Do you wish to run this test again? [y/n] ")
		if not isinstance(again, basestring):
			exit("Did not recognize your input, exiting...")

	if again == "n" or again == "N":
		flag = False

print("************************** Testing End **************************")
print("Good Bye")