import main
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

	icloud_settings = main.plist_value(str(Path.home()) + '/Library/Preferences/MobileMeAccounts.plist', 'Accounts')
	# Individual key locations
	# desktop = icloud_settings['Accounts'][0]['Services'][0]
	# family_sharing = icloud_settings['Accounts'][0]['Services'][1]
	# mobile_documents = icloud_settings['Accounts'][0]['Services'][2]
	# photo_stream = icloud_settings['Accounts'][0]['Services'][3]
	# mail_and_notes = icloud_settings['Accounts'][0]['Services'][4]
	# contacts = icloud_settings['Accounts'][0]['Services'][5]
	# calendar = icloud_settings['Accounts'][0]['Services'][6]
	# reminders = icloud_settings['Accounts'][0]['Services'][7]
	# bookmarks = icloud_settings['Accounts'][0]['Services'][8]
	# notes = icloud_settings['Accounts'][0]['Services'][9]
	# siri = icloud_settings['Accounts'][0]['Services'][10]
	# keychain = icloud_settings['Accounts'][0]['Services'][11]
	# find_my_mac = icloud_settings['Accounts'][0]['Services'][12]
	# news = icloud_settings['Accounts'][0]['Services'][13]
	# stocks = icloud_settings['Accounts'][0]['Services'][14]
	# home = icloud_settings['Accounts'][0]['Services'][15]

	for i in icloud_settings['Accounts'][0]['Services']:
		try:
			print(i['Name'], i['status'])
			icloud_plist.update({i['Name']: i['status']})

		except KeyError:
			try:
				print(i['Name'], i['Enabled'])
				icloud_plist.update({i['Name']: i['Enabled']})
			except KeyError:
				print(i)

	main.plist_create(icloud_plist, '/tmp/iCloud.plist')

