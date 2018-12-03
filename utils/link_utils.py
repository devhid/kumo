# dependency imports
from pyquery import PyQuery as pq
import tldextract as tld

# python imports
from urllib.parse import urlparse, \
                         urljoin, \
                         urldefrag
# utils imports
from utils.namedtuples import Form

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
    dtwo_ext = tld.extract(dom_two)
    if(done_ext.domain != dtwo_ext.domain):
        return False
    
    done = '.'.join(done_ext[:])
    dtwo = '.'.join(dtwo_ext[:])
    return done.find(dtwo) != -1 or dtwo.find(done) != -1

    

