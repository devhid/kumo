from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urljoin
import re


def tokenize_html(html):
    """Return all tokenized strings from an html document passed as a string

    Parameters
    ---
    html: string
        String represention of a page's html document

    Returns
    ---
    wordset: set<string>
        Set containing all the words on the current page
    """
    d = pq(html)

    wordset = set()

    sentences = d.text()

    for word in sentences.split():
        wordset.add(word)
    
    return wordset

def retrieve_links(html, base_url):
    """Return all links from an html document passed as a string

    Parameters
    ---
    html: string
        String represention of a page's html document
    base_url: string
        Url of the html document's webpage

    Returns
    ---
    wordset: set<string>
        Set containing all the links on the current page
        Relative urls are converted to absolute using the current url
    """
    d = pq(html)

    wordset = set()
    for link in d('a'):
        url = link.attrib['href']
        parsed_link = urlparse(url)
        print(url)
        if(parsed_link.netloc == ""): # Relative link
            url = urljoin(base_url, url)

        if(url[len(url) - 1] == "/"):
            url = url[0:len(url) - 1]

        wordset.add(url)

    return wordset

def detect_login(html, base_url):
    """Return all links from an html document passed as a string

    Parameters
    ---
    html: string
        String represention of a page's html document
    base_url: string
        Url of the html document's webpage

    Returns
    ---
    login: boolean
        Return whether the current page is a login 
    """
    if(len(base_url) < 8):
        return False

    # RESTful URL Standards
    url = base_url
    if(url[len(url) - 1] == "/"):
        url = url[0:len(url) - 1]
    last_param_pos = url.rfind("/")
    print(last_param_pos)
    if(last_param_pos != 7 and last_param_pos != 8): 
        last_param = url[last_param_pos + 1:len(url)]
        print(last_param)
        if(last_param == "login" or last_param == "signin"):
            return True

    # HTML Forms
    d = pq(html)
    user_input = False
    pass_input = False
    login_submit = False
    register_submit = False

    for form in d('form'):
        if(form.attrib['method'].lower() == "post"):
            for inp in d('input'):

                # Register submit button
                if((inp.attrib['value'].lower() == "register"
                or inp.attrib['value'].lower() == "signup"
                or inp.attrib['value'].lower() == "sign up")
                and inp.attrib['type'].lower() == "submit"):
                    register_submit = True

                # Login submit button
                if((inp.attrib['value'].lower() == "log in"
                or inp.attrib['value'].lower() == "login"
                or inp.attrib['value'].lower() == "signin"
                or inp.attrib['value'].lower() == "sign in")
                and inp.attrib['type'].lower() == "submit"):
                    login_submit = True

                # Username/email input
                if((inp.attrib['name'].lower() == "log in"
                or inp.attrib['name'].lower() == "login"
                or inp.attrib['name'].lower() == "log"
                or inp.attrib['name'].lower() == "user" 
                or inp.attrib['name'].lower() == "username"
                or inp.attrib['name'].lower() == "user_login"
                or inp.attrib['name'].lower() == "email"
                or inp.attrib['name'].lower() == "signin"
                or inp.attrib['name'].lower() == "sign in")
                and inp.attrib['type'].lower() == "text"):
                    user_input = True
                
                # Password input 
                if((inp.attrib['name'].lower() == "passwd"
                or inp.attrib['name'].lower() == "pass" 
                or inp.attrib['name'].lower() == "password"
                or inp.attrib['name'].lower() == "email")
                or inp.attrib['type'].lower() == "password"):
                    pass_input = True

    print(user_input)
    print(pass_input)
    print(login_submit)
    print(register_submit)
    return user_input and pass_input and login_submit
    
# HTML Forms Bootstrap
    