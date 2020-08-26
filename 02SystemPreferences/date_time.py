import subprocess
import shared
import os

if __name__ == '__main__':
	# 2.2.1 Enable "Set time and date automatically" (Scored)
	# This one requires elevated privileges to run. This isn't my favorite thing...
	# visudo user ALL=(ALL) NOPASSWD: /full/path/to/command ARG1 ARG2, /full/path/to/command ARG1 ARG2
	date_time_plist = {}
	ntp_status = subprocess.run(['sudo', 'systemsetup', '-getusingnetworktime'],
	                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "On" in ntp_status.stdout.decode('utf-8'):
		date_time_plist.update({'NetworkTime': 1})
	else:
		date_time_plist.update({'NetworkTime': 0})
	# 2.2.2 Ensure time set is within appropriate limits (Scored)
	# 2.2.3 Added my own benchmark for NTP time server
	ntp_server = subprocess.run(['sudo', 'systemsetup', '-getnetworktimeserver'],
	                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	date_time_plist.update({'NTPServer': ntp_server.stdout.decode('utf-8')[21:].rstrip("\n")})
	if os.path.isfile('/var/db/ntp-kod') is True:  # if false, needs to be created
		ntp_offset = subprocess.run(['sudo', 'sntp', '-Ss', '-M', '128', str(date_time_plist['NTPServer'])],
		                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		date_time_plist.update({'NTPOffset': ntp_offset.stdout.decode('utf-8')[97:-61]})
	shared.plist_create(date_time_plist, "/tmp/DateTime.plist")