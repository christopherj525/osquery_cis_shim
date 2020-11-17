from CIStoPLIST import shared
import subprocess
import os
from pathlib import Path

system_preferences_plist = {}


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


def date_time():
    # 2.2.1 Enable "Set time and date automatically" (Scored)
    # This one requires elevated privileges to run. This isn't my favorite thing...
    # visudo user ALL=(ALL) NOPASSWD: /full/path/to/command ARG1 ARG2, /full/path/to/command ARG1 ARG2
    date_time_plist = {}
    ntp_status = subprocess.run(['sudo', 'systemsetup', '-getusingnetworktime'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "On" in ntp_status.stdout.decode('utf-8'):
        date_time_plist.update({'NetworkTime': 1})
    else:
        date_time_plist.update({'NetworkTime': 0})
    # 2.2.2 Ensure time set is within appropriate limits (Scored)
    # 2.2.3 Added my own benchmark for NTP time server
    ntp_server = subprocess.run(['sudo', 'systemsetup', '-getnetworktimeserver'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date_time_plist.update({'NTPServer': ntp_server.stdout.decode('utf-8')[21:].rstrip("\n")})
    if os.path.isfile('/var/db/ntp-kod') is True:  # if false, needs to be created
        ntp_offset = subprocess.run(['sudo', 'sntp', '-Ss', '-M', '128', str(date_time_plist['NTPServer'])],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        date_time_plist.update({'NTPOffset': ntp_offset.stdout.decode('utf-8')[97:-61]})
    return date_time_plist


def screen_saver():
    # 2.3 Desktop & Screen Saver
    # 2.3.1 Set an inactivity interval of 20 minutes or less for the screen saver (Scored)
    screen_saver_plist = {}
    screen_saver_start_after = subprocess.run(['defaults', '-currentHost', 'read', 'com.apple.screensaver', 'idleTime'],
                                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    screen_saver_plist.update({'ScreenSaverIdleTime': int(screen_saver_start_after.stdout.decode('utf-8'))})
    # 2.3.2 Secure screen saver corners (Scored)
    screen_saver_corners = {}
    screen_saver_bl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-bl-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    screen_saver_corners.update({'ScreenSaverBLCorner': int(screen_saver_bl_corner.stdout.decode('utf-8'))})
    screen_saver_br_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-br-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    screen_saver_corners.update({'ScreenSaverBRCorner': int(screen_saver_br_corner.stdout.decode('utf-8'))})
    screen_saver_tl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tl-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    screen_saver_corners.update({'ScreenSaverTLCorner': int(screen_saver_tl_corner.stdout.decode('utf-8'))})
    screen_saver_tr_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tr-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    screen_saver_corners.update({'ScreenSaverTRCorner': int(screen_saver_tr_corner.stdout.decode('utf-8'))})
    screen_saver_plist.update({'ScreenSaverCorners': screen_saver_corners})
    return screen_saver_plist
    # 2.3.3 Familiarize users with screen lock tools or corner to Start Screen Saver (Not Scored)
    # This is user training only.


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


def security_privacy():
    # 2.6 Security & Privacy
    # This section contains recommendations for configurable options under the Security & Privacy panel.
    security_privacy_plist = {}
    # 2.6.1.1 Enable FileVault (Scored)
    fv_status = subprocess.run(['fdesetup', 'status'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "FileVault is On." in fv_status.stdout.decode('utf-8'):
        security_privacy_plist.update({'FilevaultStatus': 1})
    if "FileVault is Off." in fv_status.stdout.decode('utf-8'):
        security_privacy_plist.update({'FilevaultStatus': 0})

    # 2.6.7 Monitor Location Services Access (Not Scored)
    location_service_access = subprocess.run(['sudo', 'defaults', 'read', '/var/db/locationd/clients.plist'],
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # this isn't great, apple's clients.plist looks more like a dictionary than a plist.
    # returns a string that is difficult to parse.
    security_privacy_plist.update({'LocationServiceAccess': location_service_access.stdout.decode('utf-8')})

    # 5.15 Require an administrator password to access system-wide preferences (Scored)
    system_preferences = subprocess.Popen('security authorizationdb read system.preferences 2> /dev/null | '
                                          'grep -A1 shared | grep -E "(true|false)"',
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    system_preferences_out = system_preferences.communicate()
    security_privacy_plist.update(
        {'SecurityAuthorization': system_preferences_out[0].decode('utf-8').rstrip("\n")[2:6]})
    return security_privacy_plist


def icloud():
    # 2.7 iCloud
    # iCloud is Apple's service for synchronizing, storing and backing up data from Apple applications in both macOS
    # and iOS
    # These settings are per user, so this should run as the user.
    icloud_plist = {}
    # 2.7.1 iCloud configuration (Not Scored)
    # 2.7.2 iCloud keychain (Not Scored)
    # 2.7.3 iCloud Drive (Not Scored)
    # 2.7.4 iCloud Drive Document sync (Scored)
    # 2.7.5 iCloud Drive Desktop sync (Scored)
    icloud_settings = shared.plist_value(str(Path.home()) + '/Library/Preferences/MobileMeAccounts.plist', 'Accounts')

    for i in icloud_settings['Accounts'][0]['Services']:
        try:
            # print(i['Name'], i['status'])
            icloud_plist.update({i['Name']: i['status']})

        except KeyError:
            try:
                # print(i['Name'], i['Enabled'])
                icloud_plist.update({i['Name']: i['Enabled']})
            except KeyError:
                print(i)
    return icloud_plist


def time_machine():
    # 2.8 Time Machine
    time_machine_plist = {}
    # time_machine_settings = main.plist_value('/Library/Preferences/com.apple.TimeMachine.plist', 'AutoBackup')
    auto_backup = subprocess.run(
        ['sudo', 'defaults', 'read', '/Library/Preferences/com.apple.TimeMachine.plist', 'AutoBackup'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time_machine_plist.update({'AutoBackup': int(auto_backup.stdout.decode('utf-8').rstrip("\n"))})
    return time_machine_plist


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


def secure_keyboard():
    # 2.10 Enable Secure Keyboard Entry in terminal.app (Scored)
    secure_keyboard_plist = {}
    secure_keyboard_status = subprocess.run(['defaults', 'read', '-app', 'Terminal', 'SecureKeyboardEntry'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    secure_keyboard_plist.update({'SecureKeyboard': secure_keyboard_status.stdout.decode('utf-8').rstrip("\n")})
    return secure_keyboard_plist


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

