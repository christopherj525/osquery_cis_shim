import subprocess
from CIStoPLIST import shared

# 2.10 Enable Secure Keyboard Entry in terminal.app (Scored)
if __name__ == '__main__':
    secure_keyboard_plist = {}
    secure_keyboard_status = subprocess.run(['defaults', 'read', '-app', 'Terminal', 'SecureKeyboardEntry'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    secure_keyboard_plist.update({'SecureKeyboard': secure_keyboard_status.stdout.decode('utf-8').rstrip("\n")})
    shared.plist_create(secure_keyboard_plist, '/tmp/SecureKeyboard.plist')
