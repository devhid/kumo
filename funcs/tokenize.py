from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urljoin
from utils.constants import USER_KEYWORDS
from utils.constants import PASS_KEYWORDS
from utils.constants import LOGIN_KEYWORDS
from utils.constants import REGISTER_KEYWORDS
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
    d.make_links_absolute(base_url)
    wordset = set()
    for link in d('a'):
        url = link.attrib['href']
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
    if(detect_login_from_url(base_url)):
        return True
    
    if(html == ""):
        return False

    d = pq(html)

    # HTML Form
    user_input = False
    pass_input = False
    login_submit = False
    register_submit = False


    for form in d('form'):
        if(form.attrib['method'].lower() == "post"):
            e = pq(form)
            for inp in e('input'):
                for attrib in inp.attrib:
                    if(user_input and pass_input and login_submit):
                        break

                    # Register submit button
                    if(register_submit == False
                    and inp.attrib[attrib].lower() in REGISTER_KEYWORDS
                    and inp.attrib['type'].lower() == "submit"):
                        register_submit = True

                    # Login submit button
                    if(login_submit == False
                    and inp.attrib[attrib].lower() in LOGIN_KEYWORDS
                    and inp.attrib['type'].lower() == "submit"):
                        login_submit = True

                    # Username/email input
                    if(user_input == False
                    and inp.attrib[attrib].lower() in USER_KEYWORDS
                    and inp.attrib['type'].lower() == "text"):
                        user_input = True
                    
                    # Password input 
                    if(pass_input == False
                    and (inp.attrib[attrib].lower() in PASS_KEYWORDS
                    or inp.attrib['type'].lower() == "password")):
                        pass_input = True

    if(user_input and pass_input and login_submit):
        """
        print(user_input)
        print(pass_input)
        print(login_submit)
        print(register_submit)
        """
        return True
    
    # HTML Forms Text or Bootstrap
    for form in d('form'):
        wordset = tokenize_html(form)
        for word in wordset:
            word = word.lower()
            if(user_input == False):
                user_input = word in USER_KEYWORDS
            if(pass_input == False):
                pass_input = word in PASS_KEYWORDS
        e = pq(form)
        for button in e('button'):
            word = e(button).text().lower()
            if(login_submit == False):
                login_submit = word in LOGIN_KEYWORDS
            if(register_submit == False):
                register_submit = word in REGISTER_KEYWORDS
    """
    print(user_input)
    print(pass_input)
    print(login_submit)
    print(register_submit)
    """
    return user_input and pass_input and login_submit
    
def detect_login_from_url(base_url):
    """Determine whether a url is a login page based of RESTful path standards

    Parameters
    ---
    base_url: string
        Url of the html document's webpage

    Returns
    ---
    login: boolean
        Return whether the current page is a login 
    """

    if(len(base_url) < 8): # Less than "http://"
        return False

    # RESTful URL Standards
    url = base_url
    if(url[len(url) - 1] == "/"):
        url = url[0:len(url) - 1]
    last_param_pos = url.rfind("/")
    if(last_param_pos != 7 and last_param_pos != 8): 
        last_param = url[last_param_pos + 1:len(url)]
        if(last_param == "login" or last_param == "signin"):
            return True

    return False
