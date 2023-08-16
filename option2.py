import re
from utilities import print_colored

def get_login_credentials(html):
    users = re.findall(r'u - (.+?)\n', html)
    passwords = re.findall(r'p - (.+?)\n', html)
    emails = re.findall(r'e - (.+?)\n', html)
    return '\n'.join([f'u - {u}\np - {p}' for u, p in zip(users, passwords)])


def get_login_credentials(html):
    users = re.findall(r'u - (.+?)\n', html)
    passwords = re.findall(r'p - (.+?)\n', html)
    return '\n'.join([f'u - {u}\np - {p}' for u, p in zip(users, passwords)])

def process_option2(html):
    print_colored(get_login_credentials(html))