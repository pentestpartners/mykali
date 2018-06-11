#!/usr/bin/env python

import json
from subprocess import Popen
from pwn import log
from sys import exit
from os import chdir

stdout = open("mykali.log", 'a')

'''
Load the config.json config file in as a dictionary
'''
def load_config():
	log.info("Loading config...")
	config_file_name = "config.json"
	config_file = open(config_file_name, 'r')
	config = json.load(config_file)
	log.success("Config loaded successfully")
	return config

'''
Update the Kali distribution using apt-get.
'''
def update_kali(config):
	progress = log.progress("Updating Kali")
        process = Popen("apt-get update && apt-get full-upgrade -y", shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            progress.success("Done!")
        else:
            progress.failure("Failure...:")
            log.error("Please check the log for more information")
            exit(1)

'''
Install any packages that are required by this script (such as git).
'''
def install_requirements(config):
    progress = log.progress("Installing required packages...")
    for package in config["requirements"]:
        process = Popen("apt-get install -y %s" % package, shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            process.success("Done!")
        else:
            process.failure("Failed to install: %s" % package)
            log.error("Please check the log for more information")
            exit(1)
'''
Install any user defined git repositories.
'''
def install_git_repos(config):
    log.info("Cloning and configuring git repositories...")
    chdir(config["git"]["install_dir"])
    for repo in config["git"]["repos"]:
        url = repo["url"]
        directory = repo["directory"]
        progress = log.progress("Cloning: %s into %s" % (url, directory))
        process = Popen("git clone %s ./%s" % (url, directory), shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            progress.success("Complete.") 
        else:
            progress.failure("Failed to clone %s into %s, please check the logs" % (url, directory))
    log.success("Git cloning complete")

'''
Main method
'''
def main():
	log.info("***** mykali Kali setup script by m0rv4i *****")
	config = load_config()
        install_requirements(config)
        update_kali(config)
        install_git_repos(config)

# Entry point
if __name__ == "__main__":
	main()
