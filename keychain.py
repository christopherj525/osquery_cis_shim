import main
import subprocess

if __name__ == '__main__':
	# 5.7 Automatically lock the login keychain for inactivity (Scored)
	keychain_plist = {}
	keychain_timeout = subprocess.run(['security', 'show-keychain-info'],
	                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	keychain_plist.update({'KeychainTimeout': keychain_timeout.stdout.decode('utf-8').rstrip("\n")})

	# 5.8 Ensure login keychain is locked when the computer sleeps (Scored)
	keychain_sleep_lock = subprocess.run(['security', 'show-keychain-info'],
	                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	keychain_plist.update({'KeychainSleepLock': keychain_sleep_lock.stdout.decode('utf-8').rstrip("\n")})

	# 5.9 Enable OCSP and CRL certificate checking (Scored)
	certificate_check_CRL = subprocess.run(['defaults', 'read', 'com.apple.security.revocation', 'CRLStyle'],
	                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	keychain_plist.update({'TrustCRL': certificate_check_CRL.stdout.decode('utf-8').rstrip("\n")})

	certificate_check_OCSP = subprocess.run(['defaults', 'read', 'com.apple.security.revocation', 'OCSPStyle'],
	                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	keychain_plist.update({'TrustOCSP': certificate_check_OCSP.stdout.decode('utf-8').rstrip("\n")})

	main.plist_create(keychain_plist, "/tmp/Keychain.plist")
