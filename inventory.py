#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Ansible Dynamic Inventory script using MongoDB 
# https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html
#
# Author: BestPath <info@bestpath.io>
# Version: 0.1
# Date: 10-06-2018
#
                                           

import sys
import argparse
from pymongo import MongoClient

try:
    import json
except ImportError:
    import simplejson as json


class DynamicInventory(object):

    def __init__(self, args):
        self.inventory = {}
        self.args = args
        self.connection = MongoClient('0.0.0.0:27017')
        self.db = self.connection.ansible
        #self.db.authenticate("ansible", "ansible")
        self.cursor = self.db

        self.group_query = {}
        self.host_query = {}
        self.result = {}
        
        if self.args.list:
            self.inventory = self.dynamic_group_inventory()
            
        elif self.args.host:
            host_name = self.args.host
            self.inventory = self.dynamic_host_inventory(host_name)
            
        else:
            self.inventory = self.empty_inventory()
        
        print json.dumps(self.inventory, sort_keys=True, indent=4, separators=(",",":"))
        #print json.dumps(self.inventory, sort_keys=True, indent=2)
         
         
    def dynamic_group_inventory(self):
        result_group_query = self.cursor.groups.find(self.group_query, { '_id': False, 'name': True, 'hosts': True, 'vars': True, 'children': True })
        result_host_query = self.cursor.hosts.find(self.host_query, { '_id': False, 'hostname': True, 'vars': True })

        host_results = {}
        group_results = {}

        for host in result_host_query:
            host_results[host['hostname']] = host.get('vars', {})
            self.result = {"_meta": {"hostvars": (host_results)}}
        
        for group in result_group_query:
            self.result[group['name']] = {
                'hosts': group.get('hosts', []),
                'vars': group.get('vars', {}),
                'children': group.get('children', [])} 
               
        return self.result

        
    def dynamic_host_inventory(self, host_name):
        result_host_query = self.cursor.hosts.find({"hostname": host_name})

        host_results = {}

        for host in result_host_query:
            self.result = host.get('vars', {})

        return self.result
        
    
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host')
    args = parser.parse_args()
    DynamicInventory(args)

if __name__ == '__main__':
    main()
