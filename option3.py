import re
from utilities import print_colored

def get_key_variables(html):
    return '\n'.join(re.findall(r'\b\w*key\w*\b', html, re.IGNORECASE))

def process_option3(html):
    print_colored(get_key_variables(html))
