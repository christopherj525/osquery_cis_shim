import subprocess
import shared

# 2.13 Ensure EFI version is valid and being regularly checked (Scored)

if __name__ == '__main__':
	efi_plist = {}
	efi_status = subprocess.run(['/usr/libexec/firmwarecheckers/eficheck/eficheck', '--integrity-check'],
	                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if "No changes detected in primary hashes" in efi_status.stdout.decode('utf-8'):
		efi_plist.update({'IntegrityCheck': 'No changes detected in primary hashes'})
	else:
		efi_plist.update({'IntegrityCheck': 'Check EFI integrity'})

	shared.plist_create(efi_plist, '/tmp/EFI.plist')