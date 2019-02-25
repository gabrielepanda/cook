# Cook?

It's certainly less exquisite than a chef.


# Install

run bootstrap.sh or install directly the sshpass program
The app doesn't require any installation.
Modify the menu.yaml file and run

`python3 cook.py`


# Architecture

The cook app takes its configuration from the menu.yaml file, generates a bash
script from the configuration and runs the script on the remote host via ssh

# Configuration

The main configuration file menu.yaml has three sections

# Menus

It's a dictionary whose values are lists of task to configure a service, and
keys are the name associated with the configuration.
The list of tasks contain dictionaries with specific module configuration.
Currently only four modules are supported:

## module_name: package

installs a package. Requires the arguments

- action: install/remove
- package_name: the name of the package


## module_name: exec

Execute an arbitrary command. Requires the arguments:

- command: the command to execute

## module_name: file

Creates a file. Requires the arguments:

- path
- content
- owner (optional)
- group (optional)
- mode (optional)


## module_name: service

Interacts with systemd via systemctl. Requires the arguments:

- action: start/stop/restart
- service_name: the name of the service to handle

# Triggers

it's a dictionary whose values are normal task module described above and keys
are identifier names.
A trigger is a task module that can be called at any time from other modules
Currently file and package modules support an argument "triggers". The module
identified by the trigger will run after the original module


# Hosts

A list of dictionaries containing arguments to define to which host apply
the configuration
Parameters are:
- address: hostname or address of the host
- port: port of the host
- username
- password
- apply: is a list of configuration items to apply from the menus section so for example
`apply: [webserver]` will run the tasks defined in the `webserver` from `menus`
