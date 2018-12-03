# Python Imports
from collections import namedtuple

# bruteforce/bruteforce.py -> bruteforce()
Credential = namedtuple('Credential', ["user", "password"])

# network/HttpRequest.py -> get_status_code
StatusCode = namedtuple('StatusCode', ['status_code', 'interesting_info'])

# utils/login_utils.py -> detect_login()
Form = namedtuple('Form', ['url', 'username', 'passname', 'action'])
