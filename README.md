# ansible-mongo-inventory

# Description
Ansible Dynamic Inventory using MongoDB

## Environment

Required:
* Python 2.7
* Ansible 2.4+
* MongoDB
* Pymongo
* ArgParse

# Installation

There is no installation required for this script to work

# Usage

Ansible dynamic inventory documentation can be found at the following location:

https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html

The script is configured to return host information and group information outlined within the Ansible documentaion.

	--host <hostname> will return the specific host along with the defined variables.
	--list will return all groups and the hosts associated with each of those groups

The script can be run using any of the following options:

	./inventory.py [--host <hostname> | --list]
	python inventory.py [--host <hostname> | --list]
	ansible-inventory -i inventory.py [--host=<hostname> | --list]


## Database Layout

The script assumes that the hosts are entered into the 'hosts' collection, and the groups into the 'groups' collection using the following format:

Hosts Collection Layout:

	db.hosts.insert({"hostname": "<host_1>", "vars": {"<var_name>": "<var_attribute>", "<var_name>": "<var_attribute>"}})
	
Groups Collection Layout:

	db.groups.insert({"name": "<group_1>", "hosts": ["<host_1>"], "vars": {}, "children": []})
	db.groups.insert({"name": "<group_2>", "hosts": ["<host_2>", "<host_3>"], "vars": {}, "children": []})
	db.groups.insert({"name": "<group_3>", "hosts": [], "vars": {}, "children": ["<group_1>", "<group_2>"]})
