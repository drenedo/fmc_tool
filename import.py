import sys
import json

from command import get_parameters, get_domain, get_file, print_error_access_policy
from api import access_token, get_access_policy, post_ace_list


def main(argv):
    host, user, password, domain, policy = get_parameters(argv, False)
    file = get_file(argv)
    do_import(host, user, password, domain, policy, file)


def do_import(host, user, password, domain, policy, file_path):
    print('Making import...\n')
    print('Host: ', host)
    print('User: ', user)
    token, domains = access_token(host, user, password)
    domain_id = get_domain(domains, domain)
    access_policy = get_access_policy(host, token, domain_id, policy)
    if access_policy is not None:
        file = open(file_path, 'r')
        try:
            ace_list = json.load(file)
            post_ace_list(token, access_policy, ace_list)
        except:
            file.close()
    else:
        print_error_access_policy()


if __name__ == "__main__":
    main(sys.argv[1:])