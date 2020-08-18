import subprocess
import main

# 2.6 Security & Privacy
# This section contains recommendations for configurable options under the Security & Privacy panel.

if __name__ == '__main__':
	security_privacy_plist = {}
	# 2.6.1.1 Enable FileVault (Scored)
	fv_status = subprocess.run(['fdesetup', 'status'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "FileVault is On." in fv_status.stdout.decode('utf-8'):
		security_privacy_plist.update({'FilevaultStatus': 1})
	if "FileVault is Off." in fv_status.stdout.decode('utf-8'):
		security_privacy_plist.update({'FilevaultStatus': 0})

	# 2.6.7 Monitor Location Services Access (Not Scored)
	location_service_access = subprocess.run(['sudo', 'defaults', 'read', '/var/db/locationd/clients.plist'],
	                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# this isn't great, apple's clients.plist looks more like a dictionary than a plist.
	# returns a string that is difficult to parse.
	security_privacy_plist.update({'LocationServiceAccess': location_service_access.stdout.decode('utf-8')})

	main.plist_create(security_privacy_plist, "/tmp/SecurityAndPrivacy.plist")