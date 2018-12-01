from funcs import transform

def bruteforce(url,words):
    """ Bruteforces every combination of username and password for a specific form.

    Parameters
    ----------
    url : string
        url to send POST requests to, corresponding to a form
    words : set(string)
        set of words from which to use for bruteforcing

    Returns
    -------
    success : list((string,string))
        success will be a list of namedtuples called Credentials whose first element
        is a string denoting the username and the second element is a string denoting
        the password. The Credentials in the list denote successful attempts.
    """