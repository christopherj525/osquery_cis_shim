import subprocess
from pathlib import Path
from CIStoPLIST import shared

def screen_saver():
    # 2.3 Desktop & Screen Saver
    # 2.3.1 Set an inactivity interval of 20 minutes or less for the screen saver (Scored)
    screen_saver_plist = {}
    screen_saver_start_after = subprocess.run(['defaults', '-currentHost', 'read', 'com.apple.screensaver', 'idleTime'],
                                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        screen_saver_plist.update({'ScreenSaverIdleTime': int(screen_saver_start_after.stdout.decode('utf-8'))})
        # 2.3.2 Secure screen saver corners (Scored)
        screen_saver_corners = {}
    except ValueError:
        print("This may not work on this version of the OS")
    screen_saver_bl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-bl-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        screen_saver_corners.update({'ScreenSaverBLCorner': int(screen_saver_bl_corner.stdout.decode('utf-8'))})
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    try:
        screen_saver_br_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-br-corner'],
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except ValueError:
        print("This may not work on this version of the OS")
    try:
        screen_saver_corners.update({'ScreenSaverBRCorner': int(screen_saver_br_corner.stdout.decode('utf-8'))})
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    try:
        screen_saver_tl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tl-corner'],
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    try:
        screen_saver_corners.update({'ScreenSaverTLCorner': int(screen_saver_tl_corner.stdout.decode('utf-8'))})
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    screen_saver_tr_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tr-corner'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        screen_saver_corners.update({'ScreenSaverTRCorner': int(screen_saver_tr_corner.stdout.decode('utf-8'))})
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    try:
        screen_saver_plist.update({'ScreenSaverCorners': screen_saver_corners})
    except UnboundLocalError:
        print("This may not work on this version of the OS")
    return screen_saver_plist
    # 2.3.3 Familiarize users with screen lock tools or corner to Start Screen Saver (Not Scored)
    # This is user training only.


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
    try:
        auto_backup = subprocess.run(
            ['sudo', 'defaults', 'read', '/Library/Preferences/com.apple.TimeMachine.plist', 'AutoBackup'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except ValueError:
        print("This may not work on this version of the OS")
    try:
        time_machine_plist.update({'AutoBackup': int(auto_backup.stdout.decode('utf-8').rstrip("\n"))})
    except ValueError:
        print("This may not work on this version of the OS")
    return time_machine_plist




if __name__ == '__main__':
    print(screen_saver())
    print(icloud())
    print(time_machine())

