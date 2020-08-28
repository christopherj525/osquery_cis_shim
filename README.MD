Python scripts and Fleet configuration files to bring CIS Benchmarks for Macintosh (10.15.x) to Osquery.

This repository is part of a larger work which is evaluating the efficacy of using CIS Benchmarks with Osquery, Elastic Stack, and theHive as a means for auditing CIS Benchmark standards.

Full paper can be found here: <Insert Link>

### `CIStoPLIST` 
A series of scripts that are designed to pull system states defined by CIS benchmarks and place them into PLIST files which are readable by Osquery.

### `OsqueryFleetConfigs`
These conf files can be imported into fleet using the fleetctl command, and will run the full set of CIS Benchmarks for MacOS.

### `User` or `System`
Some values are user based and would need to run as the user, others are system level. It is important to understand which context it needs to run in.

### `sudo` Required 
Some commands must be run with sudo, adding the command via visudo 

`user ALL=(ALL) NOPASSWD: /full/path/to/command ARG1 ARG2, /full/path/to/command ARG1 ARG2`

### `Full Disk Access` Permission

In MacOS Catalina some application data is protected by the Operating System. 
For example, to check the status of 'Open "Safe" files after downloading' would be found in the terminal using 

`$ defaults read com.apple.Safari AutoOpenSafeDownloads` 

There is no means by which specific permission can be given to run this so terminal must be given `Full Disk Access`
