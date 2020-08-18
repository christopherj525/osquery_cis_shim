import plistlib
import subprocess
# Osquery seems to struggle with binary plists, in order to get the data from binary .plist files this will
# take those values and put them into an xml formatted .plist that Osquery can read.
# Created primarily from the examples at: https://docs.python.org/3/library/plistlib.html


def plist_value(in_file, key):
    """
    takes a plist file location and key and returns the key, value pair
    :param in_file: absolute path of a .plist file
    :param key: name of key to be read from the .plist file
    :return: key, value
    """
    with open(in_file, 'rb') as fp:
        pl = plistlib.load(fp)
    return {key: (pl[key])}


def plist_create(dict_of_plist_key_values, out_file):
    """
    Takes a dictionary and converts it to a plist file.
    :param dict_of_plist_key_values: a dictionary of key values you want turned into a plist.
    :param out_file: the file name and location.
    :return: None
    """
    with open(out_file, 'wb') as fp:
        plistlib.dump(dict_of_plist_key_values, fp)
    return None


if __name__ == '__main__':
    # This will be a dictionary where all the keys and values will end up
    # before being written to a final .plist file.
    plist_key_values = {}
    Bluetooth = "/Library/Preferences/com.apple.Bluetooth.plist", 'ControllerPowerState', 'PersistentPortsServices'
    plist_key_values.update(plist_value(Bluetooth[0], Bluetooth[1]))
    plist_key_values.update(plist_value(Bluetooth[0], Bluetooth[2]))
    # print(plist_key_values)
    # plist_key_values.update(
    #     defaults_values('defaults read com.apple.systemuiserver menuExtras | grep Bluetooth.menu', 'BluetoothMenu'))
    plist_create(plist_key_values, "/tmp/test.plist")
    defaults_read('BluetoothMenu', 'com.apple.systemuiserver', 'menuExtras', '|', 'grep', 'Bluetooth.menu')
    # result = subprocess.run(['defaults', 'read', 'com.apple.systemuiserver', 'menuExtras', '|', 'grep', 'Bluetooth.menu' ])
    # print(result)