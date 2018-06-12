#!/usr/bin/env python

import json
import argparse
from subprocess import Popen
from sys import exit
from os import chdir, path

class Logger:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    
    @staticmethod
    def info(message):
        print "[%s*%s] %s" % (Logger.BLUE, Logger.ENDC, message)

    @staticmethod
    def success(message):
        print "[%s+%s] %s" % (Logger.GREEN, Logger.ENDC, message)
    
    @staticmethod
    def failure(message):
        print "[%s-%s] %s" % (Logger.RED, Logger.ENDC, message)

# The log file used by the subprocesses
stdout = open("mykali.log", 'a')

'''
Load the config.json config file in as a dictionary.
'''
def load_config(directory):
	Logger.info("Loading config from %s" % directory)
        if not path.isdir(directory):
            Logger.failure("Directory does not exist, please check and try again.")
            exit(1)
	config_file = open(path.join(directory, 'config.json'), 'r')
	config = json.load(config_file)
	Logger.success("Config loaded successfully!")
        config_file.close()
	return config

'''
Check that the Kali linux sources have been set in /etc/apt/sources.list (as when you install from CD, they are not).
'''
def check_kali_sources(config):
    Logger.info("Checking sources file...")
    sources_file_path = config["kali-sources"]["sources-file"]
    if not path.isfile(sources_file_path):
        Logger.failure("Failed.")
        Logger.failure("Configured sources file does not exist, please check the config and try again.")
    sources_file = open(sources_file_path, 'a+')
    kali_repo = config["kali-sources"]["repo"]
    repo_configured = False
    for line in sources_file:
        if kali_repo in line and "#" not in line:
            repo_configured = True
            Logger.success("Already configured.")
            break
    if not repo_configured:
        sources_file.write(kali_repo)
        Logger.success("Repo added.")
    sources_file.close()

'''
Update the Kali distribution using apt-get.
'''
def update_kali(config):
	Logger.info("Updating Kali")
        process = Popen("apt-get update && apt-get full-upgrade -y", shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            Logger.success("Done!")
        else:
            Logger.failure("Failed.")
            Logger.failure("Please check the log for more information.")
            exit(1)

'''
Install any packages that are required by this script (such as git).
'''
def install_requirements(config):
    Logger.info("Installing requirements...")
    package_list = ' '.join(map(str, config["requirements"])) 
    process = Popen("apt-get install -y %s" % package_list, shell = True, stdout = stdout, stderr = stdout)
    process.wait()
    if process.returncode == 0:
        Logger.success("Done!")
    else:
        Logger.failure("Failed to install: %s" % package)
        Logger.failure("Please check the log for more information.")
        exit(1)
'''
Install any user defined packages.
'''
def install_packages(config):
    if len(config["packages"]) > 0:
        Logger.info("Installing packages...")
        package_list = ' '.join(map(str, config["packages"])) 
        process = Popen("apt-get install -y %s" % package_list, shell = True, stdout = stdout, stderr = stdout)
        process.wait()
        if process.returncode == 0:
            Logger.success("Done!")
        else:
            Logger.failure("Failed.")
            Logger.failure("Please check the log for more information.")
            exit(1)

'''
Install any user defined git repositories.
'''
def install_git_repos(config):
    if "repos" in config["git"] and len(config["git"]["repos"]) > 0:
        errored = False
        Logger.info("Cloning and configuring git repositories...")

        for repo in config["git"]["repos"]:
            chdir(config["git"]["install_dir"])
            url = repo["url"]
            directory = repo["directory"]
            Logger.info("Cloning: %s into %s" % (url, directory))

            if path.isdir(directory):
                Logger.failure("The directory exists, is it already installed?")
                continue
            
            process = Popen("git clone %s %s" % (url, directory), shell = True, stdout = stdout, stderr = stdout)
            process.wait()

            if process.returncode == 0:
                Logger.success("Complete.") 
                configure_git_repo(repo)
            else:
                Logger.failure("Failed, please check the log for more information.")
                errored = True

        # Once all is done, Logger a message depending on if any errored
        if errored:
            Logger.success("Git cloning complete, but with some errors. Please check the Logger for specifics.")
        else:
            Logger.success("Git cloning complete")

'''
Configure/install the git repos if require - e.g. run pip install or setup scripts. The exact commands are defined in the config file. 
'''
def configure_git_repo(repo):
    if "install_cmds" in repo and len(repo["install_cmds"]) > 0:
        Logger.info("Running repo setup scripts...")
        chdir(repo["directory"])
        for cmd in repo["install_cmds"]:
            process = Popen(cmd, shell = True, stdout = stdout, stderr = stdout)
            process.wait()

            if process.returncode == 0:
                Logger.success("Complete.") 
            else:
                Logger.failure("Failed, please check the log for more information.")
                break

'''
Create an arg parser for handling the program arguments.
'''
def create_arg_parser():
    parser = argparse.ArgumentParser(description = 'A Kali Linux configuration tool')
    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument("-r", "--run", help = "Run the setup with the current configuration", action="store_true")
    exclusive.add_argument("-c", "--config", help = "Display the current configuration file", action="store_true")
    parser.add_argument("-d", "--directory", help = "Specify the directory containing the config.json file.")
    return parser

'''
Main method.
'''
def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    directory = path.dirname(path.realpath(__file__)) 

    if args.directory is not None:
        directory = args.directory
        if not path.isdir(directory):
            Logger.failure("%s does not exist, please check and try again." % directory)
            exit(1)

    if args.config:
        print open(path.join(directory, 'config.json'), 'r').read()
        exit(0)

    if args.run:
        Logger.info("***** mykali Kali setup script by m0rv4i *****\n\n")
        Logger.info("Check the mykali.log file for subprocess logs.")
        config = load_config(directory)
        check_kali_sources(config)
        update_kali(config)
        install_requirements(config)
        install_packages(config)
        install_git_repos(config)
        exit(0)
    
    parser.print_help()

# Entry point
if __name__ == "__main__":
	main()
