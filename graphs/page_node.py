# dependency imports
import tldextract

# python imports
from collections import deque
import time
from urllib.parse import urlparse

# funcs imports
from funcs.tokenizer import tokenize_html

# utils imports
from utils.constants import HTTP_TOO_MANY_REQ, HTTP_RETRY_TIME
from utils.link_utils import retrieve_links, in_domain, dom_family
from utils.login_utils import detect_login

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse


class PageNode:

    def __init__(self, url):
        self.url = url
        self.connected_pages = set()
        self.login_pages = set()
        self.other_domains = set()
        self.tokenized_words = set()
        self.retries = {} # key = url of page that returned 429 or 503, value is # of tries
    
    def process(self,agent):
        status_code = 0
        self.retries[self.url] = 0
        # this loop should not have to handle a redirect, as a PageNode is only processed if
        # the status code is >= 200 and <= 300 (refer to DomainNode.process())
        while True:
            response = HttpRequest.get(self.url,agent)
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, __ = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        self.retries[self.url] += 1
                        if self.retries[self.url] >= HTTP_TOO_MANY_REQ:
                            print(f"    could not connect within {HTTP_TOO_MANY_REQ} tries.")
                            return
                        else:
                            print(f"{self.url}")
                            print(f"     was busy. retrying in {HTTP_RETRY_TIME} seconds.")
                            time.sleep(HTTP_RETRY_TIME)
                            continue
                    if status_code >= 400 and status_code <= 599:
                        return
                    break
                else:
                    return
            else:
                return

        # Retrieve all the links on the page.
        all_links = retrieve_links(response.body, self.url)
        all_links = deque(all_links)

        while all_links:
            link = all_links.popleft()
            if link in self.retries and self.retries[link] >= HTTP_TOO_MANY_REQ:
                print(f"    could not connect within {HTTP_TOO_MANY_REQ} tries.")
                continue
            response = HttpRequest.get(link,agent)

            # Continue with the next link if there are errors.
            status_code = 0
            redirect_url = ''
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, redirect_url = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        all_links.append(link)
                        self.retries[link] = 1 if link not in self.retries else self.retries[link] + 1
                        print(f"{link}")
                        print(f"    was busy. retrying in {HTTP_RETRY_TIME} seconds.")
                    if status_code >= 400 and status_code <= 599:
                        continue
                else:
                    continue
            else:
                continue

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
            
            # If the server is busy, try the request again.
            if status_code == 429 or status_code == 503:
                self.retries[link] = 1 if link not in self.retries else self.retries[link] + 1
                all_links.append(link)
                print(f"    {link} was busy. retrying in {HTTP_RETRY_TIME} seconds.")
                time.sleep(HTTP_RETRY_TIME)

            # Handle redirection by looking at the Location header.
            if status_code >= 301 and status_code <= 308:
                if in_domain(self.url, redirect_url):
                    all_links.append(redirect_url)

    def get_tokenized_words(self):
        return self.tokenized_words

    def get_other_domains(self):
        return self.other_domains
    
    def get_connected_pages(self):
        return self.connected_pages
    
    def get_login_pages(self):
        return self.login_pages

    def is_login_page(self, rel_url):
        for login in self.login_pages:
            if rel_url == login.url:
                return True
        return False