import requests
import json
import sys
import traceback
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from datetime import datetime
from sys import getsizeof

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


# Returns the access token for the api of fmc
def access_token(server, username, password):
    print('Generating Access Token...')
    auth_url = f'https://{server}/api/fmc_platform/v1/auth/generatetoken'
    try:
        # REST call with SSL verification turned off:
        r = requests.post(auth_url, headers=HEADERS, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
        print(r.status_code)
        auth_token = r.headers['X-auth-access-token']
        domains = json.loads(r.headers['DOMAINS'])
        if auth_token is None:
            print('auth_token not found. Exiting...')
            sys.exit()
    except Exception as err:
        print(f'Error in generating auth token --> {traceback.format_exc()}')
        sys.exit(3)
    return auth_token,domains


# Return headers and before add the token
def get_headers_with_token(token):
    headers = dict(HEADERS)
    headers['X-auth-access-token'] = token
    return headers


def get_access_policy(server, token, domain, name):
    print('Retrieving access policies...')
    url = f'https://{server}/api/fmc_config/v1/domain/{domain}/policy/accesspolicies?expanded=true&offset=0&limit=1000'
    headers = get_headers_with_token(token)
    acp_list = get_items(url, headers)
    print('Retrieved policies: ', len(acp_list))
    return next(filter(lambda acp: acp['name'] == name, acp_list), None)


def get_rules(token, acp):
    print('Retrieving rules...')
    url = f'{acp["rules"]["links"]["self"]}?expanded=true&offset=0&limit=1000'
    rules = get_items(url, get_headers_with_token(token))
    save_json_file(rules)
    return rules


# Collects and returns items from all pages
def get_items(url, headers):
    try:
        # REST call with SSL verification turned off
        r = requests.get(url, headers=headers, verify=False)
        status_code = r.status_code
        try:
            temp_list = r.json()['items']
        except:
            return []
        json_resp = r.json()
        if status_code == 200:
            while 'next' in json_resp['paging']:
                url_get = json_resp['paging']['next'][0]
                print(f'*\n*\nCOLLECTING NEXT PAGE... {url_get}')
                try:
                    # REST call with SSL verification turned off
                    r = requests.get(url_get, headers=headers, verify=False)
                    status_code = r.status_code
                    json_resp = r.json()
                    if status_code == 200:
                        # Loop for First Page of Items
                        for item in json_resp['items']:
                            # Append Items to New Dictionary
                            temp_list.append(item)
                except requests.exceptions.HTTPError as err:
                    print (f'Error in connection --> {traceback.format_exc()}')
    except requests.exceptions.HTTPError as err:
        print (f'Error in connection --> {traceback.format_exc()}')
    return temp_list


def save_json_file(list):
    filename = f'acp_original_rule_export_{datetime.now().strftime("%Y-%m-%d_%H%M")}.json'
    print('Save original rules to ', filename)
    outfile = open(filename, 'a')
    outfile.write(json.dumps(list, indent=4))
    outfile.close()


def post_one_by_one(token, acp, list):
    print('Importing ', len(list), ' rules to ', acp["name"])
    url = f'{acp["rules"]["links"]["self"]}'
    print(url)
    size = len(list)
    headers = get_headers_with_token(token)
    print('starting...')

    r = requests.put(url, data=json.dumps(list[0]), headers=headers, verify=False)
    process_request(r)

def post_ace_list(token, acp, list):
    print('Importing ', len(list), ' rules to ', acp["name"])
    url = f'{acp["rules"]["links"]["self"]}?bulk=true&section=default'
    print(url)
    size = len(list)
    headers = get_headers_with_token(token)
    print('starting...')
    if size > 500:
        print('Rules great than 500')
        for not_so_bulk_list in chunk(list, int(size / 500) + 1):
            print('\nNumber of rules being posted is ', len(not_so_bulk_list))
            print('Size of data being posted ', getsizeof(not_so_bulk_list), ' Bytes')
            r = requests.post(url, data=json.dumps(not_so_bulk_list), headers=headers, verify=False)
            process_request(r)
    else:
        print('Number of rules being posted is ', len(list))
        print('Size of data being posted ', getsizeof(list), ' Bytes')
        r = requests.post(url, data=json.dumps(list), headers=headers, verify=False)
        process_request(r)


def process_request(r):
    if r.status_code == 200 or r.status_code == 201:
        print("Post was successful!")
    else:
        print("Status code : Reason -->", r.status_code, ' : ', r.content)
        sys.exit(5)


def chunk(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out
