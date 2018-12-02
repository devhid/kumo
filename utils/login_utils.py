# dependency imports
from pyquery import PyQuery as pq

# python imports
from urllib.parse import urlparse, urljoin, urldefrag

# utils imports
from utils.constants import SUCCESS_KEYWORDS, \
                            USER_KEYWORDS, \
                            PASS_KEYWORDS, \
                            LOGIN_KEYWORDS, \
                            REGISTER_KEYWORDS
from utils.namedtuples import Form

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
    form_info: namedtuple Form
        Form :
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
    form_prop = ["", "", "", ""] # [form action url, user input name, password input name]
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
            form_prop[0] = form_url.path.replace('localhost', '')
            form_prop[3] = form_prop[0].replace('/', '')
            break

    if(user_input and pass_input and login_submit):
        return Form(url=form_prop[0], username=form_prop[1], 
                    passname=form_prop[2], action=form_prop[3])
    
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
            form_prop[0] = form_url.path.replace('localhost', '')
            form_prop[3] = form_prop[0].replace('/', '')
            break

    if(user_input and pass_input and login_submit):
        return Form(url=form_prop[0], username=form_prop[1], 
                    passname=form_prop[2], action=form_prop[3])
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

def verify_success_resp(words):
    """Determines if the user successfully logged in based on keywords
    Parameters
    ---
    words: set<string>
        Set of words in the page's body
    Returns
    ---
    success : boolean
        Whether the login request was successful
    """
    if len(words) == 0:
        return False

    for word in words:
        if word.lower() in SUCCESS_KEYWORDS:
            return True
    
    return False