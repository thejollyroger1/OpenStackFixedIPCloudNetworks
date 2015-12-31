#/bin/python
"""This script will pull the necessary information from the customer's API and add a fixed IP"""

import argparse
import json
import requests

class Auth:

    auth_url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    auth_headers = {'Content-type': 'application/json'}

    def __init__(self, user, api_key):
        self.user = user
        self.api_key = api_key

    def auth_call(self):
        self.auth_data = json.dumps({"auth": {'RAX-KSKEY:apiKeyCredentials': {'username': self.user, 'apiKey': self.api_key}}})
        self.auth_request = requests.post(self.auth_url, data=self.auth_data, headers=self.auth_headers)
        self.token_raw = self.auth_request.json()['access']['token']['id']
        self.token = str(self.token_raw)
        return self.token

class Subnet:

    def __init__(self, region, network_uuid, token):
        self.region = region
        self.network_uuid = network_uuid
        self.token = token

    def subnet_call(self):
        self.subnet_headers = {'X-Auth-Token': self.token}
        self.subnet_url = "https://%s.networks.api.rackspacecloud.com/v2.0/subnets" % self.region
        self.subnet_request = requests.get(self.subnet_url, headers=self.subnet_headers)
        self.subnet_return = self.subnet_request.text
        self.subnets = json.loads(self.subnet_return)['subnets']
        for networks_json in self.subnets:
            if self.network_uuid in networks_json['network_id']:
                self.subnet_id = networks_json['id']
        if self.subnet_id == "":
            print "Unable to find network based on provided UUID"
            quit()
        return self.subnet_id

def add_port(region,instance_uuid,port_name,network_uuid,ip_address,subnet_id,token,*args,**kwargs):
    port_url = 'https://%s.networks.api.rackspacecloud.com/v2.0/ports' % region
    port_data = json.dumps({"port":{"admin_state_up": "true","device_id": instance_uuid,"name": port_name,"fixed_ips": [{"ip_address": ip_address,"subnet_id": subnet_id}],"network_id": network_uuid}})
    port_headers = {'Content-Type': 'application/json','Accept': 'application/json','X-Auth-Token': token}
    port_request = requests.post(port_url, headers=port_headers, data=port_data)
    port_return = port_request.text
    print port_return

def add_virtual_interface(region,ddi,instance_uuid,network_uuid,token,*args,**kwargs):
    virt_url = 'https://%s.servers.api.rackspacecloud.com/v2/%s/servers/%s/os-virtual-interfacesv2' % (region, ddi, instance_uuid)
    virt_data = json.dumps({'virtual_interface': {'network_id': network_uuid}})
    virt_headers = {'Accept': 'application/json','Content-Type': 'application/json','X-Auth-Token': token}
    virt_request = requests.post(virt_url, headers=virt_headers, data=virt_data)
    virt_return = virt_request.text
    print virt_return


parser = argparse.ArgumentParser()

parser.add_argument('--portname',
required=False,
default="",
help='The name of the port you are creating')

parser.add_argument('--instance',
required=True,
default=None,
help='The instance UUID you want to add the IP to')

parser.add_argument('--network',
required=True,
default=None,
help='The network UUID of the private network')

parser.add_argument('--ipaddr',
required=True,
default=None,
help='The IP you want to add to the server')

parser.add_argument('--region',
required=True,
default=None,
help='The region of the server and cloud network')

parser.add_argument('--ddi',
required=True,
default=None,
help='The account number or DDI')

parser.add_argument('--user',
required=True,
default=None,
help='The user for the account')

parser.add_argument('--apikey',
required=True,
default=None,
help='The region of the server and cloud network')

args = parser.parse_args()

port_name = args.portname
instance_uuid = args.instance
user = args.user
api_key = args.apikey
ddi = args.ddi
region = args.region
ip_address = args.ipaddr
network_uuid = args.network

token_return = Auth(user,api_key)
token = token_return.auth_call()

subnet_return = Subnet(region, network_uuid, token)
subnet_id = subnet_return.subnet_call()

add_port(region,instance_uuid,port_name,network_uuid,ip_address,subnet_id,token)
add_virtual_interface(region,ddi,instance_uuid,network_uuid,token)
