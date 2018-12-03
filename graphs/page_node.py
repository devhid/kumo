
from collections import deque

from funcs.tokenizer import tokenize_html
from utils.link_utils import retrieve_links, in_domain, dom_family
from utils.login_utils import detect_login

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

from urllib.parse import urlparse
import tldextract

import time

class PageNode:

    def __init__(self, url):
        self.url = url
        self.connected_pages = set()
        self.login_pages = set()
        self.other_domains = set()
        self.tokenized_words = set()
    
    def process(self,agent):
        ext = tldextract.extract(self.url)
        dom = '.'.join(ext[:])
        dom = dom[1:] if dom[:1] == "." else dom
        relative = '/' if urlparse(self.url).path == '' else urlparse(self.url).path
                
        request = HttpRequest(dom,80,"GET")
        status_code = 0
        while True:
            response = request.send_get_request(relative,dom,agent)
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, __ = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        time.sleep(10)
                        continue
                    if status_code >= 400 and status_code <= 599:
                        return
                    else:
                        break
                else:
                    return
            else:
                return

        if self.url.find("forum.3.17.9.125.xip.io") != -1:
            print("here")
        all_links = retrieve_links(response.body, self.url)
        all_links = deque(all_links)

        while all_links:
            link = all_links.popleft()
            ext = tldextract.extract(link)
            dom = '.'.join(ext[:])
            if dom[:1] == ".":
                dom = dom[1:]
            relative = '/' if urlparse(link).path == '' else urlparse(link).path
            relative = relative.replace("\r","")
            request = HttpRequest(dom,80,"GET")
            response = request.send_get_request(relative,dom,agent)

            # Continue wtih the next link if there are errors.
            status_code = 0
            redirect_url = ''
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, redirect_url = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        all_links.append(link)
                    if status_code >= 400 and status_code <= 599:
                        continue
                else:
                    continue
            else:
                continue

            # Handle redirection by looking at the Location header.
            if status_code >= 301 and status_code <= 308:

                if in_domain(self.url, redirect_url):
                    inner_ext = tldextract.extract(redirect_url)
                    inner_dom = '.'.join(inner_ext[:])
                    inner_dom = inner_dom[1:] if inner_dom[:1] == "." else inner_dom
                    inner_relative = '/' if urlparse(redirect_url).path == '' \
                                        else urlparse(redirect_url).path
                    if inner_relative.find("\r") != -1:
                        inner_relative = inner_relative.replace("\r","")      
                    inner_request = HttpRequest(inner_dom,80,"GET")
                    inner_response = inner_request.send_get_request(inner_relative,inner_dom,agent)

                    # Continue wtih the next link if there are errors.
                    inner_status_code = 0
                    inner_redirect_url = ''
                    if inner_response is not None:
                        inner_status_tuple = inner_response.status_code
                        if inner_status_tuple is not None:
                            inner_status_code, inner_redirect_url = inner_status_tuple
                            inner_status_code = int(inner_status_code)
                            if inner_status_code == 429 or inner_status_code == 503:
                                all_links.append(redirect_url)
                            if inner_status_code >= 400 and inner_status_code <= 599:
                                continue
                        else:
                            continue
                    else:
                        continue

                    if inner_status_code >= 200 and inner_status_code <= 300:
                        url = redirect_url
                        if inner_status_code == 300:
                            url = inner_redirect_url
                        login_page = detect_login(inner_response.body, url)
                        self.connected_pages.add(url)
                        if login_page:
                            self.login_pages.add(login_page)
                        
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