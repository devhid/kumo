# Python Imports
from collections import namedtuple

# bruteforce/bruteforce.py -> bruteforce()
Credential = namedtuple('Credential', ["user", "password"])

# network/HttpRequest.py -> get_status_code
StatusCode = namedtuple('StatusCode', ['status_code', 'interesting_info'])

# utils/login_utils.py -> detect_login()
<<<<<<< HEAD
Form = namedtuple('Form', ['url', 'username', 'passname', 'action'])
=======
Form = namedtuple('Form', ['url', 'username', 'passname', 'action', 'host'])
>>>>>>> 78fb569b4649acb6a8585327c72a7692477be7d7
