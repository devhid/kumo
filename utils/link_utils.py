from utils.constants import *

from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
import tldextract as tld
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
    d('svg').remove()
    wordset = set()

    sentences = d('body').text()

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
        defrag_result = urldefrag(url) # Remove url fragment
        url = defrag_result.url
        if(url[len(url) - 1] == "/"):
            url = url[0:len(url) - 1]
        wordset.add(url)
    return wordset

def detect_login(html, base_url):
    """Return all links from an html document passed as a string

    Compares all input tag attribute values and button text in the post forms of a webpage 
    with predefined constants in utils/constant.py to determine whether the form contains
    a username input field, password input field, and a login submit button which would
    indicate that the form is a login page.

    Parameters
    ---
    html: string
        String represention of a page's html document
    base_url: string
        Url of the html document's webpage

    Returns
    ---
    form_prop: 3 element array
        0: FORM_
    """

    #if(detect_login_from_url(base_url)):
    #    return True
    
    if(html == "" or len(base_url) < 8):
        return None

    form_prop = ["", "", ""] # [form action url, user input name, password input name]

    d = pq(html)

    # HTML Form (Standard HTML)
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
                        form_prop[USER_INPUT_NAME] = inp.attrib['id']
                        user_input = True
                    
                    # Password input 
                    if(pass_input == False
                    and (inp.attrib[attrib].lower() in PASS_KEYWORDS
                    or inp.attrib['type'].lower() == "password")):
                        form_prop[PASS_INPUT_NAME] = inp.attrib['id']
                        pass_input = True

        if(user_input and pass_input):
            if('action' in form.attrib):
                form_prop[FORM_URL] = form.attrib['action']
            else:
                form_prop[FORM_URL] = base_url
            break

    if(user_input and pass_input and login_submit):
        return form_prop
    
    # HTML Forms (Bootstrap)
    for form in d('form'):
        wordset = tokenize_html(form)
        """
        for word in wordset:
            word = word.lower()
            if(user_input == False):
                user_input = word in USER_KEYWORDS
                if(user_input):
                    form_prop[USER_INPUT_NAME] = .attrib['name']
            if(pass_input == False):
                pass_input = word in PASS_KEYWORDS
                if(pass_input):
                    form_prop[PASS_INPUT_NAME] = .attrib['name']
        """

        e = pq(form)
        for button in e('button'):
            word = e(button).text().lower()
            if(login_submit == False):
                login_submit = word in LOGIN_KEYWORDS
            if(register_submit == False):
                register_submit = word in REGISTER_KEYWORDS

        if(user_input and pass_input and login_submit):
            if('action' in form.attrib):
                form_prop[FORM_URL] = form.attrib['action'] 
            break

    if(user_input and pass_input and login_submit):
        return form_prop
    else:
        return None
    
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

def in_domain(domain, url):
    """Determine whether a url resides within the provided domain

    Parameters
    ---
    domain: string
        Domain or subdomain of a webpage
    url: string
        Url of the webpage to be checked

    Returns
    ---
    login: boolean
        Return whether the url's root domain is equivalent to the provided domain
    """

    dom_ext = tld.extract(domain)
    url_ext = tld.extract(url)
    return dom_ext.subdomain == url_ext.subdomain and dom_ext.domain == url_ext.domain

def fetch_login_fields(html, base_url):
    """Return all links from an html document passed as a string

    Compares all input tag attribute values and button text in the post forms of a webpage 
    with predefined constants in utils/constant.py to determine whether the form contains
    a username input field, password input field, and a login submit button which would
    indicate that the form is a login page.

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
    # if(detect_login_from_url(base_url)):
    #     return True
    
    if(html == ""):
        return (False, None, None, None)

    d = pq(html)

    # HTML Form names
    user_input = None
    pass_input = None
    login_submit = None
    register_submit = None

    for form in d('form'):
        if(form.attrib['method'].lower() == "post"):
            e = pq(form)
            for inp in e('input'):
                for attrib in inp.attrib:
                    if(user_input and pass_input and login_submit):
                        break

                    # Register submit button
                    if(register_submit == None
                    and inp.attrib[attrib].lower() in REGISTER_KEYWORDS
                    and inp.attrib['type'].lower() == "submit"):
                        register_submit = inp.attrib['name']

                    # Login submit button
                    if(login_submit == None
                    and inp.attrib[attrib].lower() in LOGIN_KEYWORDS
                    and inp.attrib['type'].lower() == "submit"):
                        login_submit = inp.attrib['name']

                    # Username/email input
                    if(user_input == None
                    and inp.attrib[attrib].lower() in USER_KEYWORDS
                    and inp.attrib['type'].lower() == "text"):
                        user_input = inp.attrib['name']
                    
                    # Password input 
                    if(pass_input == None
                    and (inp.attrib[attrib].lower() in PASS_KEYWORDS
                    or inp.attrib['type'].lower() == "password")):
                        pass_input = inp.attrib['name']

    if (user_input and pass_input):
        return (True, user_input, pass_input, login_submit)
    
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

    return (user_input and pass_input and login_submit, user_input, pass_input, login_submit)

def verify_success_resp(html):
    """Determines if the user successfully logged in based on keywords

    Parameters
    ---
    html: string
        String represention of a page's html document

    Returns
    ---
    success : boolean
        Whether the login request was successful
    """
    d = pq(html)
    
    sentences = d.text()[30:]

    for word in sentences.split():
        if word.lower() in SUCCESS_KEYWORDS:
            return True
    
    return False