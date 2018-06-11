# mykali

**This is a WIP, it's not even at version 1.0 yet!**

## Linux setup tool for Kali Linux.

Are you tired of configuring and reconfiguring your Kali box across computers? Or getting things back "just the way you like it" after a VM dies or your hard-drive is wiped? Then maybe this is the tool for you!

*mykali*  is a Kali linux configuration tool. 

## Configuration

All the configuration is stored in the **config.json** file.

TODO

## Running

Simple: Run the script

`./mykali.py`

## Roadmap

- [ ] Have the script check the /etc/apt/sources.list is up to date (in case install from CD)
- [x] Have the script update Kali 
- [x] Have the script clone a configurable list of git repos 
- [ ] Have the script install tools from the distro repos
- [ ] Have the script run any necessary extra install commands for the git repos, such as pip/setup/extra linking
- [ ] Have the script be able to run custom commands from the configuration file
- [ ] Have the script be able to manage installing config files in some way (how?)
