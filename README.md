# mykali

**This is a WIP, it's not even at version 1.0 yet!**

## Linux setup tool for Kali Linux.

Are you tired of configuring and reconfiguring your Kali box across computers? Or getting things back "just the way you like it" after a VM dies or your hard-drive is wiped? Then maybe this is the tool for you!

*mykali*  is a Kali linux configuration tool for quickly getting the box up to scratch just the way you like it. 

All you have to do is keep the **config.json** up to date with your desired configuration and you can run it quickly and easily on other boxes to get them up to scratch.

## Configuration

The idea here is you have a google drive/dropbox/git repository with your dotfiles etc. and a **config.json**. You can then run the tool, point at that directory and it will configure the Kali box accordingly. 

TODO explain config.json

## Install

Installation can be done by running the `install.sh` script from the repository directory.

## Running

To get help run the script without args or with the `-h` or `--help` option:
```
# ./mykali.py
usage: mykali.py [-h] [-r | -c] [-d DIRECTORY]

A Kali Linux configuration tool

optional arguments:
  -h, --help            show this help message and exit
  -r, --run             Run the setup with the current configuration
  -c, --config          Display the current configuration file
  -d DIRECTORY, --directory DIRECTORY
                        Specify the directory containing the config.json file.
```

To view the current config, run the script with `-c` or `--config`:

```
# ./mykali.py --config
{
        "kali-sources" : {
                "sources-file" : "/etc/apt/sources.list",
                "repo" : "deb http://http.kali.org/kali kali-rolling main contrib non-free"
        },
        "requirements" : [
                "git"
        ],
        "packages" : [
                "byobu",
                "python-pip"
        ],
        "git" : {
                "install_dir": "/opt",
                "repos" : [
                        {
                                "directory" : "seclists",
                                "url" : "https://github.com/danielmiessler/SecLists.git"
                        },
                        {
                                "directory" : "ebowla",
                                "url" : "https://github.com/Genetic-Malware/Ebowla.git"
                        },
                        {
                                "directory" : "impacket",
                                "url" : "https://github.com/CoreSecurity/impacket",
                                "install_cmds" : [
                                        "pip install -r requirements.txt",
                                        "python setup.py install"
                                ]
                        }
                ]
        }

}
```

To run the script with the current config use the `-r` or `--run` option:
```
./mykali.py --run
```

To run the script and specify the directory holding the config files, use the `-d` or `--directory` option:

```
./mykali.py --run --directory ~/Downloads/config
```

## Roadmap

- [x] Have the script check the /etc/apt/sources.list is up to date (in case install from CD)
- [x] Have the script update Kali 
- [x] Have the script clone a configurable list of git repos 
- [x] Have the script install tools from the distro repos
- [x] Have the script run any necessary extra install commands for the git repos, such as pip/setup/extra linking
- [x] Have the script take a directory parameter for backed up config directories
- [ ] It's a bit daft we need an install script to install stuff so remove that
- [ ] Have the script be able to run custom commands from the configuration file
- [ ] Have the script be able to manage installing config files (.zshrc, .bashrc etc)
- [ ] Have the script handle environment variables for paths etc.
- [ ] Create a secondary tool for looping through an existing /opt directory (or wherever) and adding the repos to the config.json
- [ ] Set the resolution
- [ ] If a VM install VMware tools
- [ ] Install a background/wallpaper
- [ ] Look into a host script for VMs which will configure the VM appropriately (bridged/NAT'd etc)
- [ ] Another tool for mass updating git repositories 
- [ ] Set shell
- [ ] Change root password (from prompt, not config.json!)


Pull requests and/or suggestions welcome.
