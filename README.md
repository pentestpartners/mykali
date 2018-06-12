# mykali

**This is a WIP, it's not even at version 1.0 yet!**

## Linux setup tool for Kali Linux.

Are you tired of configuring and reconfiguring your Kali box across computers? Or getting things back "just the way you like it" after a VM dies or your hard-drive is wiped? Then maybe this is the tool for you!

*mykali*  is a Kali linux configuration tool for quickly getting the box up to scratch just the way you like it. 

All you have to do is keep the **config.json** up to date with your desired configuration and you can run it quickly and easily on other boxes to get them up to scratch.

## Configuration

The idea is here is you have a google drive/dropbox/git repository with your dotfiles etc. and a **config.json**. You can then run the tool, point at that directory and it will configure the Kali box accordingly. 

TODO

## Running

To get help run the script without args or with the `-h` or `--help` option:
```
./mykali.py
```

To view the current config, run the script with `-c` or `--config`:

```
./mykali.py --config
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
- [ ] Have the script be able to run custom commands from the configuration file
- [ ] Have the script be able to manage installing config files (.zshrc, .bashrc etc)
- [ ] Have the script handle environment variables for paths etc.
- [ ] Create a secondary tool for looping through an existing /opt directory (or wherever) and adding the repos to the config.json


Pull requests and/or suggestions welcome.
