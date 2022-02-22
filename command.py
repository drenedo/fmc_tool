import sys
import getopt
import getpass

from os.path import exists


# Get command line parameters and password
def get_parameters(argv, export=True):
    host = None
    user = None
    domain = None
    access_policy = None
    try:
        opts, args = getopt.getopt(argv, "h:u:d:a:f:")
    except getopt.GetoptError as e:
        print(e)
        print_help(export)
    for opt, arg in opts:
        if opt == '-h':
            host = arg
        elif opt == '-u':
            user = arg
        elif opt == '-d':
            domain = arg
        elif opt == '-a':
            access_policy = arg
    if host is not None and user is not None:
        return host, user, get_password(), domain, access_policy
    else:
        print_help(export)


# Get file from parameters
def get_file(argv):
    file = None
    try:
        opts, args = getopt.getopt(argv, "h:u:d:a:f:")
    except getopt.GetoptError:
        print_import_help()
    for opt, arg in opts:
        if opt == '-f':
            file = arg
    if file is not None and exists(file):
        return file
    else:
        if file is None:
            print('file not found')
            print_help(False)
        else:
            print('File not exits')
            sys.exit(5)


# Get password from prompt
def get_password():
    return getpass.getpass("Password: ")


# Exit and print help
def print_help(export):
    if export:
        print('export.py -h <hostname> -u <user> -d <domain> -a <access policy>')
    else:
        print('import.py -h <hostname> -u <user> -d <domain> -a <access policy> -f <json_file>')
    sys.exit(2)


# Exit and print help
def print_import_help():
    print('import.py -h <hostname> -u <user> -d <domain> -a <access policy> -f <json_file>')
    sys.exit(2)


# Get domain or raise error if there are more than one
def get_domain(domains, domain):
    print('Domains in server ', len(domains))
    if len(domains) > 1 and domain is not None:
        domain = next(filter(lambda d: d['name'] == domain, domains), None)
        if domain is None:
            print_error_domain()
        else:
            return domain['uuid']
    elif len(domains) > 1 and domain is None:
        print_error_domain()
    else:
        print('Get default domain')
        return domains[0]['uuid']


# Exit and print domain error
def print_error_domain():
    print('There are more than one domain, please set one')
    sys.exit(4)


# Exit and print access policy error
def print_error_access_policy():
    print('There are more than one access policy, please set one')
    sys.exit(5)
