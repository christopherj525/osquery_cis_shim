import subprocess
import main

if __name__ == '__main__':
	# 5.23 System Integrity Protection status (Scored)
	system_integrity_plist = {}
	system_integrity_status = subprocess.run(['/usr/bin/csrutil', 'status'],
	                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	system_integrity_plist.update(
		{'SystemIntegrityStatus': system_integrity_status.stdout.decode('utf-8').rstrip("\n")[36:-1]})
	main.plist_create(system_integrity_plist, '/tmp/SystemIntegrity.plist')
