#!/usr/bin/env python

import subprocess
import json
from pwn import log
import sys
import os

config = None
DEVNULL = open(os.devnull, 'w')

def load_config():
	log.info("Loading config...")
	config_file_name = "config.json"
	config_file = open(config_file_name, 'r')
	config = json.load(config_file)
	log.success("Config loaded successfully")
	return config

def update_kali(config):
	progress = log.progress("Updating Kali")
        if config["verbose"] == False:
            stdout = DEVNULL
        else:
            stdout = None 
        process = subprocess.Popen("apt update && apt full-upgrade -y", shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            progress.success("Done!")
        else:
            progress.failure("Failure...:")
            log.error(process.read())
            sys.exit(1)

def install_requirements(config):
    progress = log.progress("Installing required packages...")
    if config["verbose"] == False:
        stdout = DEVNULL
    else:
        stdout = None
    process = subprocess.Popen("apt install -y git", shell = True, stdout = stdout, stderr = stdout)
    process.wait()
    if process.returncode == 0:
        process.success("Done!")
    else:
        process.failure("Failed to install git")
        log.error(process.read())
        sys.exit(1)
        

def install_git_repos(config):
    os.chdir(config["git"]["install_dir"])
    for repo in config["git"]["repos"]:
        log.info("Installing: " + repo["directory"])

       

def main():
	log.info("***** mykali Kali setup script by m0rv4i *****")
	global config
	config = load_config()
        update_kali(config)
        install_git_repos(config)

# Entry point
if __name__ == "__main__":
	main()
