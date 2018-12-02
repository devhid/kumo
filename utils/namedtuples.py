from collections import namedtuple

Credential = namedtuple('Credential', ["user", "password"])
Form = namedtuple('Form', ['url', 'userid', 'passid', 'action'])
