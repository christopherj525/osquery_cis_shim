import subprocess
import os


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


if __name__ == '__main__':
    # need to run tests as root
    print(date_time())
    print(security_privacy())