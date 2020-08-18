import main
import subprocess

if __name__ == '__main__':
	# 2.1.1 Turn off Bluetooth, if no paired devices exist (Scored)
	bluetooth_plist = {}
	Bluetooth = "/Library/Preferences/com.apple.Bluetooth.plist", 'ControllerPowerState'
	bluetooth_plist.update(main.plist_value(Bluetooth[0], Bluetooth[1]))
	if bluetooth_plist['ControllerPowerState'] == 1:
		bt_power_state = subprocess.run(['system_profiler', 'SPBluetoothDataType'],
		                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		if 'Bluetooth:' and "Connectable:" in bt_power_state.stdout.decode('utf-8'):
			bluetooth_plist.update({'ControllerPowerState': "enabled and devices present"})
		else:
			bluetooth_plist.update({'ControllerPowerState': "disabled and no devices present"})
	# 2.1.2 Bluetooth "Discoverable" is only available when Bluetooth preference pane is open (Not Scored)
	# 2.1.3 Show Bluetooth status in menu bar (Scored)
	bt_status = subprocess.run(['defaults',  'read', 'com.apple.systemuiserver',  'menuExtras'],
	                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "Bluetooth.menu" in bt_status.stdout.decode('utf-8'):
		bluetooth_plist.update({'BluetoothMenu': 1})
	else:
		bluetooth_plist.update({'BluetoothMenu': 0})
	main.plist_create(bluetooth_plist, "/tmp/Bluetooth.plist")


