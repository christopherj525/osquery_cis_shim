import subprocess
import shared

# 2.11 Java 6 is not the default Java runtime (Scored)

if __name__ == '__main__':
	java_version_plist = {}
	java_version = subprocess.run(['java', '-version'],
	                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	java_version_plist.update({'JavaVersion': java_version.stdout.decode('utf-8')})

	shared.plist_create(java_version_plist, "/tmp/JavaVersion.plist")
