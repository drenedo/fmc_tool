import sys
import json
from datetime import datetime

from command import get_parameters, get_domain, print_error_access_policy
from api import access_token, get_access_policy, get_rules


def main(argv):
    host, user, password, domain, policy = get_parameters(argv)
    do_export(host, user, password, domain, policy)


def do_export(host, user, password, domain, policy):
    print('Making export...\n')
    print('Host: ', host)
    print('User: ', user)
    token, domains = access_token(host, user, password)
    domain_id = get_domain(domains, domain)
    access_policy = get_access_policy(host, token, domain_id, policy)
    if access_policy is not None:
        print('Get rules from access policy ', access_policy['name'])
        rules = get_rules(token, access_policy)
        clean_rules(rules)
        save_clean_json_file(rules)
    else:
        print_error_access_policy()


def save_clean_json_file(list):
    filename = f'acp_rule_export_{datetime.now().strftime("%Y-%m-%d_%H%M")}.json'
    print('Save cleaned rules to ', filename)
    outfile = open(filename, 'a')
    outfile.write(json.dumps(list, indent=4))
    outfile.close()


def clean_rules(rules):
    for rule in rules:
        rule.pop('metadata')
        rule.pop('links')
        rule.pop('id')
        if 'users' in rule:
            for user_obj in rule['users']['objects']:
                user_obj.pop('realm')
        if 'variableSet' in rule:
            rule['variableSet'].pop('id')
        if 'commentHistoryList' in rule:
            comments = rule['commentHistoryList']
            new_comments = []
            for comment in comments:
                new_comments.append(comment['comment'])
            rule['newComments'] = new_comments
            rule.pop('commentHistoryList')


if __name__ == "__main__":
    main(sys.argv[1:])