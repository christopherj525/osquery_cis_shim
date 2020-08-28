import subprocess
from CIStoPLIST import shared

if __name__ == '__main__':
	# 5.11 Do not enable the "root" account (Scored)
	users_accounts_plist = {}

	root_disabled = subprocess.Popen('dscl . -read /Users/root AuthenticationAuthority',
	                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	root_disabled_out = root_disabled.communicate()
	users_accounts_plist.update({'RootDisabled': root_disabled_out[0].decode('utf-8').rstrip("\n")})

	# 5.16 Disable ability to login to another user's active and locked session (Scored)
	disable_login_other_user = subprocess.Popen('/usr/bin/security authorizationdb read system.login.screensaver '
	                                            '2>/dev/null | /usr/bin/grep -A 1 "<array>" | /usr/bin/awk -F "<|>" '
	                                            '"END{ print $3 }"', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
	                                            shell=True)
	disable_login_other_user_out = disable_login_other_user.communicate()
	users_accounts_plist.update(
		{'DisableLoginUserActiveSession': disable_login_other_user_out[0].decode('utf-8')[10:-10]})

	# 5.20 Disable Fast User Switching (Not Scored)

	fast_user_switching = subprocess.run(['defaults', 'read', '/Library/Preferences/.GlobalPreferences',
	                                      'MultipleSessionEnabled'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	users_accounts_plist.update({'FastUserSwitching': bool(fast_user_switching.stdout.decode('utf-8'))})
	shared.plist_create(users_accounts_plist, '/tmp/UserAccounts.plist')