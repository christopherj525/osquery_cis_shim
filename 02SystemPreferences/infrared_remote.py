import subprocess
import shared

# 2.9 Pair the remote control infrared receiver if enabled (Scored)

if __name__ == '__main__':
	infrared_remote_plist = {}
	system_profiler_status = subprocess.run(['system_profiler'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "IR Receiver" in system_profiler_status.stdout.decode('utf-8'):
		infrared_remote_plist.update({})
		device_enabled = subprocess.run(
			['defaults', 'read', '/Library/Preferences/com.apple.driver.AppleIRController', 'DeviceEnabled'],
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		uid_filter = subprocess.run(
			['defaults', 'read', '/Library/Preferences/com.apple.driver.AppleIRController', 'UIDFilter'],
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		print(device_enabled.stdout.decode('utf-8'))
		print(uid_filter.stdout.decode('utf-8'))
	else:
		infrared_remote_plist.update({'IRReciever': 'Off'})

	shared.plist_create(infrared_remote_plist, "/tmp/InfraredReceiver.plist")
