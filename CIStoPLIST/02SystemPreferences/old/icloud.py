from CIStoPLIST import shared
from pathlib import Path

# 2.7 iCloud
# iCloud is Apple's service for synchronizing, storing and backing up data from Apple applications in both macOS and iOS
# These settings are per user, so this should run as the user.
if __name__ == '__main__':
	icloud_plist = {}
	# 2.7.1 iCloud configuration (Not Scored)
	# 2.7.2 iCloud keychain (Not Scored)
	# 2.7.3 iCloud Drive (Not Scored)
	# 2.7.4 iCloud Drive Document sync (Scored)
	# 2.7.5 iCloud Drive Desktop sync (Scored)

	icloud_settings = shared.plist_value(str(Path.home()) + '/Library/Preferences/MobileMeAccounts.plist', 'Accounts')


	for i in icloud_settings['Accounts'][0]['Services']:
		try:
			print(i['Name'], i['status'])
			icloud_plist.update({i['Name']: i['status']})

		except KeyError:
			try:
				# print(i['Name'], i['Enabled'])
				icloud_plist.update({i['Name']: i['Enabled']})
			except KeyError:
				print(i)

	shared.plist_create(icloud_plist, '/tmp/iCloud.plist')

