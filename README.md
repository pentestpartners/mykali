# mykali

**This is a WIP, it's not even at version 1.0 yet!**

## Linux setup tool for Kali Linux.

Are you tired of configuring and reconfiguring your Kali box across computers? Or getting things back "just the way you like it" after a VM dies or your hard-drive is wiped? Then maybe this is the tool for you!

*mykali*  is a Kali linux configuration tool for quickly getting the box up to scratch just the way you like it. 

All you have to do is keep the **config.json** up to date with your desired configuration and you can run it quickly and easily on other boxes to get them up to scratch.

## Configuration

All the configuration is stored in the **config.json** file.

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

## Roadmap

- [ ] Have the script check the /etc/apt/sources.list is up to date (in case install from CD)
- [x] Have the script update Kali 
- [x] Have the script clone a configurable list of git repos 
- [ ] Have the script install tools from the distro repos
- [x] Have the script run any necessary extra install commands for the git repos, such as pip/setup/extra linking
- [ ] Have the script be able to run custom commands from the configuration file
- [ ] Have the script be able to manage installing config files in some way (how?)
- [ ] Have the script handle environment variables for paths etc.
- [ ] Create a secondary tool for looping through an existing /opt directory (or wherever) and adding the repos to the config.json


Pull requests and/or suggestions welcome.
