from CIStoPLIST import shared
import subprocess

if __name__ == '__main__':
	# 6.1 Accounts Preferences Action Items
	accounts_and_environment_plist = {}

	# 6.1.1 Display login window as name and password (Scored)
	show_full_name = shared.plist_value('/Library/Preferences/com.apple.loginwindow.plist', 'SHOWFULLNAME')
	accounts_and_environment_plist.update(show_full_name)

	# 6.1.2 Disable "Show password hints" (Scored)
	try:
		retries_until_hint = shared.plist_value('/Library/Preferences/com.apple.loginwindow.plist', 'RetriesUntilHint')
		accounts_and_environment_plist.update(retries_until_hint)
	except KeyError:
		retries_until_hint = {'RetriesUntilHint': "Not Set"}
		accounts_and_environment_plist.update(retries_until_hint)
	# 6.1.3 Disable guest account login (Scored)
	guest_enabled = shared.plist_value('/Library/Preferences/com.apple.loginwindow.plist', 'GuestEnabled')
	accounts_and_environment_plist.update(guest_enabled)

	# 6.1.4 Disable "Allow guests to connect to shared folders" (Scored)
	try:
		guest_access = shared.plist_value('/Library/Preferences/com.apple.AppleFileServer.plist', 'guestAccess')
		accounts_and_environment_plist.update(guest_access)
	except KeyError:
		accounts_and_environment_plist.update({'guestAccess': 'Not Configured'})
	try:
		allow_guest_access = shared.plist_value(
			'/Library/Preferences/com.apple.AppleFileServer.plist', 'AllowGuestAccess')
		accounts_and_environment_plist.update(allow_guest_access)
	except KeyError:
		accounts_and_environment_plist.update({'AllowGuestAccess': 'Not Configured'})

	# 6.1.5 Remove Guest home folder (Scored)
	remove_guest_home_folder = subprocess.run(['ls', '/Users/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if 'Guest' in remove_guest_home_folder.stdout.decode('utf-8'):
		accounts_and_environment_plist.update({'GuestHomeFolder': 1})
	else:
		accounts_and_environment_plist.update({'GuestHomeFolder': 0})

	# 6.2 Turn on filename extensions (Scored)
	file_extensions = subprocess.run(['defaults', 'read', 'NSGlobalDomain', 'AppleShowAllExtensions'],
	                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	accounts_and_environment_plist.update(
		{'AppleShowAllExtensions': int(file_extensions.stdout.decode('utf-8').rstrip("\n"))})

	# 6.3 Disable the automatic run of safe files in Safari (Scored)
	# this setting is protected behind system preferences > security and privacy > full disk access > terminal.app
	try:
		open_safe_downloads = subprocess.run(['defaults', 'read', 'com.apple.Safari', 'AutoOpenSafeDownloads'],
		                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		accounts_and_environment_plist.update(
			{'AutoOpenSafeDownloads': int(open_safe_downloads.stdout.decode('utf-8').rstrip("\n"))})
	except TypeError:
		accounts_and_environment_plist.update({'AutoOpenSafeDownloads': "Unable to get setting"})

	plugin_first_visit = subprocess.Popen('defaults read ~/Library/Preferences/com.apple.safari.plist | '
	                                      'grep -i "PlugInFirstVisitPolicy = *"',
	                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	plugin_first_visit_out = plugin_first_visit.communicate()
	if "PlugInFirstVisitPolicy" in plugin_first_visit_out[0].decode('utf-8'):
		accounts_and_environment_plist.update({'PlugInFirstVisitPolicy': "PlugInFirstVisitPolicy"})
	else:
		accounts_and_environment_plist.update({'PlugInFirstVisitPolicy': "Not Found"})

	shared.plist_create(accounts_and_environment_plist, '/tmp/AccountsAndEnvironment.plist')



