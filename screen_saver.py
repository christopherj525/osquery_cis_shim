import main
import subprocess


if __name__ == '__main__':
	# 2.3 Desktop & Screen Saver
	# 2.3.1 Set an inactivity interval of 20 minutes or less for the screen saver (Scored)
	screen_saver_plist = {}
	screen_saver_start_after = subprocess.run(['defaults', '-currentHost', 'read', 'com.apple.screensaver', 'idleTime'],
	                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	screen_saver_plist.update({'ScreenSaverIdleTime': int(screen_saver_start_after.stdout.decode('utf-8'))})

	# 2.3.2 Secure screen saver corners (Scored)
	screen_saver_corners = {}
	screen_saver_bl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-bl-corner'],
	                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	screen_saver_corners.update({'ScreenSaverBLCorner': int(screen_saver_bl_corner.stdout.decode('utf-8'))})

	screen_saver_br_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-br-corner'],
	                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	screen_saver_corners.update({'ScreenSaverBRCorner': int(screen_saver_br_corner.stdout.decode('utf-8'))})

	screen_saver_tl_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tl-corner'],
	                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	screen_saver_corners.update({'ScreenSaverTLCorner': int(screen_saver_tl_corner.stdout.decode('utf-8'))})

	screen_saver_tr_corner = subprocess.run(['defaults', 'read', 'com.apple.dock', 'wvous-tr-corner'],
	                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	screen_saver_corners.update({'ScreenSaverTRCorner': int(screen_saver_tr_corner.stdout.decode('utf-8'))})

	print(screen_saver_plist)
	screen_saver_plist.update({'ScreenSaverCorners': screen_saver_corners})
	print(screen_saver_plist)
	# 2.3.3 Familiarize users with screen lock tools or corner to Start Screen Saver (Not Scored)
	# This is user training only.

	# 2.3.4 Ensure Password is enabled when screen saver activates
	# Not a CIS Benchmark for OSX but it is implied by the previous Benchmarks but not explicitly defined.

	main.plist_create(screen_saver_plist, "/tmp/ScreenSaver.plist")