#  FMC Tool

A simple way to export and import access rules from Cisco Firepower

## Usage

### Export

The export process generates two files, ona file with the original response and another with cleaned response.

You could omit domain or access policy if there are only one.

```
python export.py -h <hostname> -u <user> -d <domain> -a <access policy>
```

- __hostname__: The hostname or the ip address of the API.
- __user__: The user of the API. Password muy be given by prompt.
- __domain__: The domain of Cisco Firepower. Not mandatory.
- __access policiy__: The access policiy of Cisco Firepower. Not mandatory.

Common output generated:

```
$ python export.py -h 192.168.122.251 -u admin -a Source-ACP1
Password: 
Making export...

Host:  192.168.122.251
User:  admin
Generating Access Token...
204
Domains in server  1
Get default domain
Retrieving access policies...
Retrieved policies:  2
Get rules from access policy  Source-ACP-1
Retrieving rules...
Save original rules to  acp_original_rule_export_2022-02-22_2244.json
Save cleaned rules to  acp_rule_export_2022-02-22_2244.json
``` 


### Import

The import process needs a json file.

You could omit domain or access policy if there are only one.

```
import.py -h <hostname> -u <user> -d <domain> -a <access policy> -f <json_file>
```

- __hostname__: The hostname or the ip address of the API.
- __user__: The user of the API. Password muy be given by prompt.
- __domain__: The domain of Cisco Firepower. Not mandatory.
- __access policiy__: The access policiy of Cisco Firepower. Not mandatory.
- __json_file__ : The relative or the absolute path of the file with the rules. 

Common output generated:

```
$ python import.py -h 192.168.122.251 -u admin -a Destination-ACP1 -f acp_rule_export_2022-02-22_2244.json
Password: 
Making import...

Host:  192.168.122.251
User:  admin
Generating Access Token...
204
Domains in server  1
Get default domain
Retrieving access policies...
Retrieved policies:  2
Importing  429  rules to  Destination-ACP1
https://192.168.122.251/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/525400ED-840B-0ed3-0000-008589936618/accessrules?bulk=true&section=default
starting...
Number of rules being posted is  429
Size of data being posted  3704  Bytes
Post was successful!

```