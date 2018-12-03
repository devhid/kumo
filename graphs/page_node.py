import requests
from funcs.tokenizer import tokenize_html
from utils.link_utils import retrieve_links, in_domain, dom_family
from utils.login_utils import detect_login

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

from urllib.parse import urlparse
import tldextract

class PageNode:

    def __init__(self, url):
        self.url = url
        self.connected_pages = set()
        self.login_pages = set()
        self.other_domains = set()
        self.tokenized_words = set()
    
    def process(self,agent):
        ext = tldextract.extract(self.url)
        dom = ext.domain
        relative = urlparse(self.url).path
        request = HttpRequest(self.url,80,"GET")
        response = request.send_get_request(relative,dom,agent)
        status_code = 0
        if response is not None:
            status_tuple = response.status_code
            if status_tuple is not None:
                status_code, __ = status_tuple
                if status_code >= 400 and status_code <= 599:
                    return
            else:
                return
        else:
            return

        all_links = retrieve_links(response.body, self.url)

        for link in all_links:
            ext = tldextract.extract(link)
            dom = ext.domain
            relative = urlparse(link).path
            request = HttpRequest(link,80,"GET")
            response = request.send_get_request(relative,dom,agent)

            # Continue wtih the next link if there are errors.
            status_code = 0
            redirect_url = ''
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, redirect_url = status_tuple
                    if status_code >= 400 and status_code <= 599:
                        continue
                else:
                    continue
            else:
                continue

            # Handle redirection by looking at the Location header.
            if status_code >= 301 and status_code <= 308:

                if in_domain(self.url, redirect_url):

                    inner_request = HttpRequest(redirect_url,80,"GET")
                    inner_ext = tldextract.extract(self.url)
                    inner_relative = inner_ext.domain
                    inner_dom = urlparse(redirect_url).path
                    inner_response = inner_request.send_get_request(inner_relative,inner_dom,agent)

                    # Continue wtih the next link if there are errors.
                    inner_status_code = 0
                    inner_redirect_url = ''
                    if inner_response is not None:
                        inner_status_tuple = inner_response.status_code
                        if inner_status_tuple is not None:
                            inner_status_code, inner_redirect_url = inner_status_tuple
                            if inner_status_code >= 400 and inner_status_code <= 599:
                                continue
                        else:
                            continue
                    else:
                        continue

                    if inner_status_code == 200 or inner_status_code == 300:
                        login_page = detect_login(inner_response.body, inner_redirect_url)
                        if login_page:
                            self.login_pages.add(login_page)

                        self.connected_pages.add(inner_redirect_url)
                        self.tokenized_words.update(tokenize_html(inner_response.body,False))

            # Handle status 300 the same as 200.
            if status_code >= 200 and status_code <= 300:
                if in_domain(self.url, link):
                    login_page = detect_login(response.body, link)
                    if login_page:
                        self.login_pages.add(login_page)

                    self.connected_pages.add(link)
                    self.tokenized_words.update(tokenize_html(response.body,False))
                elif dom_family(self.url, link):
                    if link not in self.other_domains:
                        self.other_domains.add(link)
                else:
                    continue

    def get_tokenized_words(self):
        return self.tokenized_words

    def get_other_domains(self):
        return self.other_domains
    
    def get_connected_pages(self):
        return self.connected_pages
    
    def get_login_pages(self):
        return self.login_pages