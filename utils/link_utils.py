from utils.constants import *
from utils.namedtuples import Form

from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
import urllib.robotparser
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
    start = html.find("<!doctype html>")
    if(start == -1):
        start = html.find("<html")

    html = html[start:]

    d = pq(html)
    d('svg').remove()
    d('script').remove()
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
        if 'href' in link.attrib:
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
    form_info: namedtuple File
        File :
            url: string
                Url that the form posts to
                The url is relative to the domain
            username: string
                HTML name of the username input tag
            passname: string
                HTML name of the password input tag
    """

    #if(detect_login_from_url(base_url)):
    #    return True
    
    if(html == "" or len(base_url) < 8):
        return None

    d = pq(html)

    # HTML Form (Standard HTML)
    form_prop = ["", "", ""] # [form action url, user input name, password input name]
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
                        form_prop[1] = inp.attrib['name']
                        user_input = True
                    
                    # Password input 
                    if(pass_input == False
                    and (inp.attrib[attrib].lower() in PASS_KEYWORDS
                    or inp.attrib['type'].lower() == "password")):
                        form_prop[2] = inp.attrib['name']
                        pass_input = True

        if(user_input and pass_input):
            form_url = base_url
            if('action' in form.attrib):
                form_url = form.attrib['action']
            form_url = urlparse(form_url)
            form_prop[0] = form_url.path
            break

    if(user_input and pass_input and login_submit):
        return Form(url=form_prop[0], username=form_prop[1], passname=form_prop[2])
    
    # HTML Forms (Bootstrap)
    for form in d('form'):
        # wordset = tokenize_html(form)
        # for word in wordset:
        #     word = word.lower()
        #     if(user_input == False):
        #         user_input = word in USER_KEYWORDS
        #         if(user_input):
        #             form_prop[USER_INPUT_NAME] = .attrib['name']
        #     if(pass_input == False):
        #         pass_input = word in PASS_KEYWORDS
        #         if(pass_input):
        #             form_prop[PASS_INPUT_NAME] = .attrib['name']
        e = pq(form)
        for button in e('button'):
            word = e(button).text().lower()
            if(login_submit == False):
                login_submit = word in LOGIN_KEYWORDS
            if(register_submit == False):
                register_submit = word in REGISTER_KEYWORDS

        if(user_input and pass_input and login_submit):
            form_url = base_url
            if('action' in form.attrib):
                form_url = form.attrib['action']
            form_url = urlparse(form_url)
            form_prop[0] = form_url.path
            break

    if(user_input and pass_input and login_submit):
        return Form(url=form_prop[0], username=form_prop[1], passname=form_prop[2])
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
        last_param = url[last_param_pos + 1:]
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

def dom_family(dom_one, dom_two):
    """Determine the relation of one domain to another

    Parameters
    ---
    dom_one: string
        Domain or subdomain of a webpage
    dom_two: string
        Domain or subdomain of a webpage

    Returns
    ---
    login: boolean
        Return whether domain_one and domain_two are in the same domain family
    """

    done_ext = tld.extract(dom_one)
    # print(done_ext)
    dtwo_ext = tld.extract(dom_two)
    # print(dtwo_ext)
    if(done_ext.domain != dtwo_ext.domain):
        return False
    
    done = '.'.join(done_ext[:])
    # print(done)
    dtwo = '.'.join(dtwo_ext[:])
    # print(dtwo)

    if done == dtwo:
        return False
    return done.find(dtwo) != -1 or dtwo.find(done) != -1

def clean_url(url):
    if url[-1] == '/':
        return url[:-1]
    
    return url

def get_domain(url):

    o = urlparse(url)
    link = o.scheme + "://" + o.netloc
    return link

def add_subdomain(url, subdomain):
    o = urlparse(url)

    return o.scheme + "://" + subdomain.strip() + "." + o.netloc + o.path

def get_robot_links(html, base_url):
    rp = urllib.robotparser.RobotFileParser()
    
    rp.parse(html.decode('utf-8').splitlines())

    paths = [clean_url(base_url + str(rule).split()[1]) for rule in rp.default_entry.rulelines]
    
    return paths

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
    if len(html) == 0:
        return False
    d = pq(html)
    
    sentences = d.text()[30:]

    for word in sentences.split():
        if word.lower() in SUCCESS_KEYWORDS:
            return True
    
    return False
    

