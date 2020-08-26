import subprocess
import re
import shared

# 5.2 Password Management

if __name__ == '__main__':
	password_policy_plist = {}

	# 5.2.1 Configure account lockout threshold (Scored)
	failed_logins = subprocess.Popen("pwpolicy -getaccountpolicies | "
	                                 "grep -A 1 'policyAttributeMaximumFailedAuthentications' | "
	                                 "tail -1 | cut -d'>' -f2 | cut -d '<' -f1" ,
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
	pass_age = subprocess.Popen('pwpolicy -getaccountpolicies | egrep policyAttributeExpiresEveryNDays', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
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

	shared.plist_create(password_policy_plist, '/tmp/PasswordPolicy.plist')
