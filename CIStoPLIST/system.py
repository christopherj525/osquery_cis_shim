import subprocess
import re
from CIStoPLIST import shared



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


def network_configuration():
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
    return network_configurations_plist


def password_policy():
    password_policy_plist = {}

    # 5.2.1 Configure account lockout threshold (Scored)
    failed_logins = subprocess.Popen("pwpolicy -getaccountpolicies | "
                                     "grep -A 1 'policyAttributeMaximumFailedAuthentications' | "
                                     "tail -1 | cut -d'>' -f2 | cut -d '<' -f1",
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    failed_logins_out = failed_logins.communicate()
    password_policy_plist.update({'MaxFailedLoginAttempts': int(failed_logins_out[0].decode('utf-8'))})

    # 5.2.2 Set a minimum password length (Scored)
    min_pass_lenth = subprocess.Popen('pwpolicy -getaccountpolicies | egrep "15 characters"',
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    min_pass_lenth_out = min_pass_lenth.communicate()
    if "15 characters" in min_pass_lenth_out[0].decode('utf-8'):
        password_policy_plist.update({'MinimumPasswordLength': 15})
    else:
        password_policy_plist.update({'MinimumPasswordLength': 0})

    # 5.2.3 Complex passwords must contain an Alphabetic Character (Not Scored)
    pass_contains_alpha = subprocess.Popen('pwpolicy -getaccountpolicies | egrep "Alpha"',
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pass_contains_alpha_out = pass_contains_alpha.communicate()
    if "com.apple.policy.legacy.requiresAlpha" in pass_contains_alpha_out[0].decode('utf-8'):
        password_policy_plist.update({'PasswordRequiresAlpha': 1})
    else:
        password_policy_plist.update({'PasswordRequiresAlpha': 0})

    # 5.2.4 Complex passwords must contain a Numeric Character (Not Scored)
    pass_contains_numeric = subprocess.Popen('pwpolicy -getaccountpolicies | egrep "Numeric"',
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pass_contains_numeric_out = pass_contains_numeric.communicate()
    if "com.apple.policy.legacy.requiresNumeric" in pass_contains_numeric_out[0].decode('utf-8'):
        password_policy_plist.update({'PasswordRequiresNumeric': 1})
    else:
        password_policy_plist.update({'PasswordRequiresNumeric': 0})

    # 5.2.5 Complex passwords must contain a Special Character (Not Scored)
    pass_contains_special = subprocess.Popen('pwpolicy -getaccountpolicies | egrep "1 special"',
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pass_contains_special_out = pass_contains_special.communicate()
    if "Password must have at least 1 special character" in pass_contains_special_out[0].decode('utf-8'):
        password_policy_plist.update({'PasswordRequiresSpecial': 1})
    else:
        password_policy_plist.update({'PasswordRequiresSpecial': 0})

    # 5.2.6 Complex passwords must uppercase and lowercase letters (Not Scored)
    pass_contains_upper_lower = subprocess.Popen('pwpolicy -getaccountpolicies | '
                                                 'egrep "com.apple.uppercaseAndLowercase"',
                                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pass_contains_upper_lower_out = pass_contains_upper_lower.communicate()
    if "com.apple.uppercaseAndLowercase" in pass_contains_upper_lower_out[0].decode('utf-8'):
        password_policy_plist.update({'PasswordRequiresUpperAndLower': 1})
    else:
        password_policy_plist.update({'PasswordRequiresUpperAndLower': 0})

    # 5.2.7 Password Age (Scored)
    pass_age = subprocess.Popen('pwpolicy -getaccountpolicies | egrep policyAttributeExpiresEveryNDays',
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    pass_age_out = pass_age.communicate()

    if "policyAttributeExpiresEveryNDays" in pass_age_out[0].decode('utf-8'):
        password_age = re.findall(r'[0-9]+', pass_age_out[0].decode('utf-8'))
        password_policy_plist.update({'PasswordAge': pass_age})
    else:
        password_policy_plist.update({'PasswordAge': 0})

    # 5.2.8 Password History (Scored)
    differ_from_past = subprocess.Popen('pwpolicy -getaccountpolicies | egrep "differ from past"',
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    differ_from_past_out = differ_from_past.communicate()
    if "Password must differ from past 15 passwords" in differ_from_past_out[0].decode('utf-8'):
        password_policy_plist.update({'DifferFromPast': 15})
    else:
        password_policy_plist.update({'DifferFromPast': 0})
    return password_policy_plist


def system_integrity():
    # 5.23 System Integrity Protection status (Scored)
    system_integrity_plist = {}
    system_integrity_status = subprocess.run(['/usr/bin/csrutil', 'status'],
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    system_integrity_plist.update(
        {'SystemIntegrityStatus': system_integrity_status.stdout.decode('utf-8').rstrip("\n")[36:-1]})
    return system_integrity_plist


def user_account_status():
    # needs to be tested.
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
    return users_accounts_plist


if __name__ == '__main__':
    system_plist = {}
    # system_plist.update(bluetooth())
    # system_plist.update(energy_saver())
    # system_plist.update(infrared_remote())
    # system_plist.update(java())
    # system_plist.update(efi())
    system_plist.update(network_configuration())
    system_plist.update(password_policy())
    system_plist.update(system_integrity())
    system_plist.update(user_account_status())
    print(system_plist)
    shared.plist_create('/tmp/system_cis.plist', system_plist)

