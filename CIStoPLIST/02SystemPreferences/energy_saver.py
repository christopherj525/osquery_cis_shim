import subprocess
from CIStoPLIST import shared

# 2.5 Energy Saver
# This section contains recommendations related to the configurable items under the Energy Saver panel

if __name__ == '__main__':
	# 2.5.1 Disable "Wake for network access" (Scored)
	energy_saver_plist = {}
	wake_status = subprocess.run(['pmset', '-g'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "womp                 0" in wake_status.stdout.decode('utf-8'):
		energy_saver_plist.update({'WakeForNetworkAccess': 0})
	if "womp                 1" in wake_status.stdout.decode('utf-8'):
		energy_saver_plist.update({'WakeForNetworkAccess': 1})
	# 5.14 Ensure system is set to hibernate (Scored)
	hibernate = subprocess.Popen('pmset -g | egrep standbydelay', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
	                             shell=True)
	hibernate_out = hibernate.communicate()
	energy_saver_plist.update({'HibernateDelay': hibernate_out[0].decode('utf-8').rstrip("\n")})

	shared.plist_create(energy_saver_plist, "/tmp/EnergySaver.plist")