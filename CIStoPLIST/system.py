import subprocess
import os
from CIStoPLIST import shared


# Beginning of the "System Preferences Block, relating to CIS 02
# Additional controls are found in system_elevated.py and user.py
def bluetooth():
    """
    :return: a dictionary of settings for writing to a plist file.
    """
    # 2.1.1 Turn off Bluetooth, if no paired devices exist (Scored)
    bluetooth_plist = {}
    bluetooth = "/Library/Preferences/com.apple.Bluetooth.plist", 'ControllerPowerState'
    bluetooth_plist.update(shared.plist_value(bluetooth[0], bluetooth[1]))
    if bluetooth_plist['ControllerPowerState'] == 1:
        bt_power_state = subprocess.run(['system_profiler', 'SPBluetoothDataType'],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if 'Bluetooth:' and "Connectable:" in bt_power_state.stdout.decode('utf-8'):
            bluetooth_plist.update({'ControllerPowerState': "enabled and devices present"})
        else:
            bluetooth_plist.update({'ControllerPowerState': "disabled and no devices present"})
    # 2.1.2 Bluetooth "Discoverable" is only available when Bluetooth preference pane is open (Not Scored)
    # 2.1.3 Show Bluetooth status in menu bar (Scored)
    bt_status = subprocess.run(['defaults', 'read', 'com.apple.systemuiserver', 'menuExtras'],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "Bluetooth.menu" in bt_status.stdout.decode('utf-8'):
        bluetooth_plist.update({'BluetoothMenu': 1})
    else:
        bluetooth_plist.update({'BluetoothMenu': 0})
    return bluetooth_plist


def energy_saver():
    # 2.5 Energy Saver
    # This section contains recommendations related to the configurable items under the Energy Saver panel
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
    return energy_saver_plist


def infrared_remote():
    # 2.9 Pair the remote control infrared receiver if enabled (Scored)
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
    return infrared_remote_plist


def java():
    # 2.11 Java 6 is not the default Java runtime (Scored)
    java_version_plist = {}
    java_version = subprocess.run(['java', '-version'],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    java_version_plist.update({'JavaVersion': java_version.stdout.decode('utf-8')})
    return java_version_plist


def efi():
    # 2.13 Ensure EFI version is valid and being regularly checked (Scored)
    efi_plist = {}
    efi_status = subprocess.run(['/usr/libexec/firmwarecheckers/eficheck/eficheck', '--integrity-check'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "No changes detected in primary hashes" in efi_status.stdout.decode('utf-8'):
        efi_plist.update({'IntegrityCheck': 'No changes detected in primary hashes'})
    else:
        efi_plist.update({'IntegrityCheck': 'Check EFI integrity'})
    return efi_plist
# End of System Preferences block, relating to  CIS 02


if __name__ == '__main__':
    system_plist = {}
    system_plist.update(bluetooth())
    system_plist.update(energy_saver())
    system_plist.update(infrared_remote())
    system_plist.update(java())
    system_plist.update(efi())
    print(system_plist)
    shared.plist_create('/tmp/system_cis.plist', system_plist)

