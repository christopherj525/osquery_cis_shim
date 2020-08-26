import shared
import subprocess

# 2.8 Time Machine

if __name__ == '__main__':
	time_machine_plist = {}

	# time_machine_settings = main.plist_value('/Library/Preferences/com.apple.TimeMachine.plist', 'AutoBackup')

	auto_backup = subprocess.run(
		['sudo', 'defaults', 'read', '/Library/Preferences/com.apple.TimeMachine.plist', 'AutoBackup'],
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	time_machine_plist.update({'AutoBackup': int(auto_backup.stdout.decode('utf-8').rstrip("\n"))})
	print(time_machine_plist)

	shared.plist_create(time_machine_plist, "/tmp/TimeMachine.plist")
