#!/usr/bin/env python

import json
import argparse
from subprocess import Popen
from pwn import log
from sys import exit
from os import chdir, path

# The log file used by the subprocesses
stdout = open("mykali.log", 'a')

'''
Load the config.json config file in as a dictionary
'''
def load_config():
	log.info("Loading config...")
	config_file = open('config.json', 'r')
	config = json.load(config_file)
	log.success("Config loaded successfully")
        config_file.close()
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
            progress.success("Done!")
        else:
            process.failure("Failed to install: %s" % package)
            log.error("Please check the log for more information")
            exit(1)

'''
Install any user defined git repositories.
'''
def install_git_repos(config):
    errored = False
    log.info("Cloning and configuring git repositories...")

    for repo in config["git"]["repos"]:
        chdir(config["git"]["install_dir"])
        url = repo["url"]
        directory = repo["directory"]
        progress = log.progress("Cloning: %s into %s" % (url, directory))

        if path.isdir(directory):
            progress.failure("The directory already exists, is it already installed?")
            continue
        
        process = Popen("git clone %s %s" % (url, directory), shell = True, stdout = stdout, stderr = stdout)
        process.wait()

        if process.returncode == 0:
            progress.success("Complete.") 
            configure_git_repo(repo)
        else:
            progress.failure("Failed, please check the log.")
            errored = True

    # Once all is done, log a message depending on if any errored
    if errored:
        log.success("Git cloning complete, but with some errors. Please check the log for specifics.")
    else:
        log.success("Git cloning complete")

'''
Configure/install the git repos if require - e.g. run pip install or setup scripts. The exact commands are defined in the config file. 
'''
def configure_git_repo(repo):
    if "install_cmds" in repo and len(repo["install_cmds"]) > 0:
        progress = log.progress("Running repo setup scripts...")
        chdir(repo["directory"])
        for cmd in repo["install_cmds"]:
            process = Popen(cmd, shell = True, stdout = stdout, stderr = stdout)
            process.wait()

            if process.returncode == 0:
                progress.success("Complete.") 
            else:
                progress.failure("Failed, please check the log.")
                break

'''
Create an arg parser for handling the program arguments
'''
def create_arg_parser():
    parser = argparse.ArgumentParser(description = 'A Kali Linux configuration tool')
    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument("-r", "--run", help = "Run the setup with the current configuration", action="store_true")
    exclusive.add_argument("-c", "--config", help = "Display the current configuration file", action="store_true")
    return parser

'''
Main method
'''
def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    if args.config:
        print open("%s/config.json" % path.dirname(__file__),"r").read()
        exit(0)

    if args.run:
        log.info("***** mykali Kali setup script by m0rv4i *****\n\n")
        log.info("Check the mykali.log file for subprocess logs")
        config = load_config()
        install_requirements(config)
        update_kali(config)
        install_git_repos(config)
        exit(0)
    
    parser.print_help()

# Entry point
if __name__ == "__main__":
	main()
