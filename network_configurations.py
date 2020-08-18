import subprocess
import main

# 4 Network Configurations

if __name__ == '__main__':
	# 4.1 Disable Bonjour advertising service
	# the key "NoMulticastAdvertisements" does not exist by default.
	network_configurations_plist = {}
	bonjour_disabled = subprocess.run(['defaults', 'read', '/Library/Preferences/com.apple.mDNSResponder.plist',
	                                   'NoMulticastAdvertisements'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	network_configurations_plist.update(
		{'BonjourDisabled': {'BonjourDisabled': bonjour_disabled.stdout.decode('utf-8')}})

	wifi_menu = subprocess.Popen('defaults read com.apple.systemuiserver menuExtras | grep AirPort.menu',
	                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	wifi_menu_out = wifi_menu.communicate()
	network_configurations_plist.update({'WiFiStatus': wifi_menu_out[0].decode('utf-8').rstrip("\n")})

	network_locations = subprocess.run(['networksetup', '-listlocations'],
	                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	network_configurations_plist.update({'NetworkLocations': network_locations.stdout.decode('utf-8').rstrip("\n")})

	http_server_status = subprocess.Popen('ps -ef | grep -i [h]ttpd',
	                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	http_server_status_out = http_server_status.communicate()
	network_configurations_plist.update({'HTTPServerStatus': http_server_status_out[0].decode('utf-8')})

	nfs_server_status = subprocess.Popen('ps -ef | grep -i [n]fsd',
	                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	nfs_server_status_out = nfs_server_status.communicate()
	network_configurations_plist.update({'NFSServerStatus': nfs_server_status_out[0].decode('utf-8'.rstrip("\n"))})

	nfs_server_export = subprocess.run(['cat', '/etc/exports'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	network_configurations_plist.update({'NFSServerExport': nfs_server_export.stdout.decode('utf-8').rstrip("\n")})
	main.plist_create(network_configurations_plist, '/tmp/NetworkCgti onfiguration.plist')