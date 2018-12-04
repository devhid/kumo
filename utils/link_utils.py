# dependency imports
from pyquery import PyQuery as pq
import tldextract as tld

# python imports
from urllib.parse import urlparse, \
                         urljoin, \
                         urldefrag
import urllib.robotparser

# utils imports
from utils.namedtuples import Form, RequestInfo

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
    """ Strips the ending / from a URL if it exists.

    Parameters
    ----------
    url : string
        HTTP URL

    Returns
    -------
    url : string
        URL that is stripped of an ending / if it existed
    """
    if url[-1] == '/':
        return url[:-1]
    
    return url

def get_domain(url):
    """ Get the domain from a URL.

    Parameters
    ----------
    url : string
        HTTP URL

    Returns
    -------
    domain : string
        domain of the URL
    """
    o = urlparse(url)
    scheme = o.scheme

    if not o.scheme:
        scheme = "http"

    link = scheme + "://" + o.netloc
    return link

def add_subdomain(url, subdomain):
    """ Adds a subdomain to a URL.

    Parameters
    ----------
    url : string
        HTTP URL
    subdomain : string
        subdomain to append to the front of a URL

    Returns
    -------
    domain : string
        combined URL and subdomain
    """
    o = urlparse(url)
    scheme = o.scheme

    if not o.scheme:
        scheme = "http"

    link = scheme + "://" + subdomain.strip() + "." + o.netloc + o.path

    return link

def get_robot_links(html, base_url):
    """ Get the robots.txt links given the HTML body of the file and the base URL.

    Parameters
    ----------
    html : string
        HTML body of the robots.txt file
    base_url : string
        base URL of the domain

    Returns
    -------
    paths : list(string)
        list of paths from the robots.txt file
    """
    rp = urllib.robotparser.RobotFileParser()
    
    rp.parse(html.splitlines())
    
    paths = []

    if rp.default_entry:
        paths = [clean_url(base_url + str(rule).split()[1]) for rule in rp.default_entry.rulelines]
    
    return paths

def extract_host_rel(url):
    """ Extract the [host] and [relative_url] that would be used in an HTTP request.

    Parameters
    ----------
    url : string
        HTTP URL

    Returns
    -------
    request_info : RequestInfo (namedtuple)
        first value is the [host] and second is the [relative_url]
    """
    if url.find("https://") != -1:
        url = url.replace("https://","http://")
    elif url.find("http://") == -1:
        url = "http://" + url
    ext = tld.extract(url)
    dom = '.'.join(ext[:])
    dom = dom[1:] if dom[:1] == "." else dom
    rel = urlparse(url).path
    relative = '/' if rel == '' else rel
    relative = relative.replace("\r","")
    return RequestInfo(host=dom,rel_url=relative)

