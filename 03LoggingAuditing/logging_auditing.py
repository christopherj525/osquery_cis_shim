import subprocess
import shared

# 3 Logging and Auditing

if __name__ == '__main__':
	# 3.2 Configure Security Auditing Flags (Scored)
	audit_plist = {}
	audit_flags = subprocess.Popen('sudo grep ^flags /etc/security/audit_control',
	                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	audit_flags_out = audit_flags.communicate()
	audit_plist.update({'AuditFlags': audit_flags_out[0].decode('utf-8').rstrip("\n")[6:]})

	audit_retention = subprocess.Popen('sudo cat /etc/security/audit_control | egrep expire-after',
	                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	audit_retention_out = audit_retention.communicate()
	audit_plist.update({'AuditRetention': audit_retention_out[0].decode('utf-8')})

	install_log = subprocess.Popen('grep -i ttl /etc/asl/com.apple.install',
	                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	install_log_out = install_log.communicate()
	if 'ttl=365' in install_log_out[0].decode('utf-8'):
		audit_plist.update({'InstallLogRetention': 1})
	else:
		audit_plist.update({'InstallLogRetention': 0})

	shared.plist_create(audit_plist, '/tmp/LoggingAuditing.plist')
