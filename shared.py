import plistlib


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