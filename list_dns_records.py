# Script to list all DNS records for an account and output as csv

import json
import requests
import getpass
import csv

# Username/password to authenticate against the API
username = ""
password = "" # Leave this blank if you don't want it in plaintext and it'll prompt you to input it when running the script. 

# API URL
base_url = ""

# Param validation
if not username:
    username = input("Username: ")

if not password:
    passwd = getpass.getpass('Password:')
else:
    passwd = password

if not base_url:
    base_url = input("Base URL (EX: http://localhost:8001 or http://45.59.252.4:8001): ")

# Full URL
login_url = base_url + '/v2/public/user/login'

# Shorthand helper function
def get_auth_token():
    response = requests.post(
        url=login_url,
        data=json.dumps({"username": username, "password": passwd}),
        headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
        })
    return response.json()['session_id']

auth_token = get_auth_token()

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json',
    'X-Auth-Token': auth_token
}

# Get DNS Zone info
def get_zones(offset):
    data = {
        "selected_resource_type": "dnszone",
        "scopes": [],
        "filters": [],
        "offset": offset,
        "limit": limit,
        "tags": [],
        "insight_exemptions": False,
        "counts": {}
    }
    response = requests.post(
        url=base_url + '/v2/public/resource/query',
        data=json.dumps(data),
        headers=headers
        )
    return response.json()    

# Get DNS Zone info
def get_records(resource_id):
    data = {}
    response = requests.post(
        url=base_url + '/v2/public/dnszone/' + resource_id + '/dnsrecords/list',
        data=json.dumps(data),
        headers=headers
        )
    return response.json()    

## Make as many calls as necessary to get all of the info. Max response limit is 100
offset = 0
limit = 100
zone_info = get_zones(offset)
zone_count = zone_info['counts']['dnszone']

if zone_count > limit:
    calls, remainder= divmod(zone_count, limit)
    if remainder > 0:
            calls += 1
    
    for x in range(calls):
        next_zone_info = get_zones(offset)
        offset = offset + limit
        zone_info['resources'].extend(next_zone_info['resources'])

# Create a CSV
with open('dns_records.csv', mode='w') as csv_file:
    fieldnames = ['domain', 'account_name', 'account_id', 'cloud', 'is_private', 'record_name', 'record_type', 'record_data']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through all the zones)
    for zone in zone_info['resources']:
        domain = zone['dnszone']['domain']
        resource_id = zone['dnszone']['common']['resource_id']
        account_name = zone['dnszone']['common']['account']
        account_id = zone['dnszone']['common']['account_id']
        cloud = zone['dnszone']['common']['cloud']
        is_private = zone['dnszone']['is_private_zone']

        # Add in an entry for every record in the zone
        record_info = get_records(resource_id)
        for record in record_info['dnsrecords']:
            record_name = record['common']['resource_name']
            record_type = record['record_type']
            record_data = record['data']

            writer.writerow({'domain': domain, 'account_name': account_name, 'account_id': account_id, 'cloud': cloud, 'is_private': is_private, 'record_name': record_name, 'record_type': record_type, 'record_data': record_data})

