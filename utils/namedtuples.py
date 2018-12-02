from collections import namedtuple

Credential = namedtuple('Credential', ["user", "password"])
Form = namedtuple('Form', ['url', 'userid', 'passid', 'action'])
StatusCode = namedtuple('StatusCode', ['status_code', 'interesting_info'])