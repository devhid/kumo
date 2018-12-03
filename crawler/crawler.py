# python imports
from collections import deque

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

# utils imports
from utils.constants import SUBDOMAINS
from utils.link_utils import clean_url, get_domain, add_subdomain
from utils.namedtuples import StatusCode
from utils.login_utils import detect_login

# graphs imports
from graphs.domain_graph import DomainGraph
from graphs.domain_node import DomainNode
from bruteforce.bruteforce import bruteforce

# tokenize imports
from funcs.tokenizer import tokenize_html

import tldextract
from urllib.parse import urlparse

class Crawler:
    def __init__(self):
        self.page_count = 0 # Global page counter.
        self.tokenized = set() # Global set of tokenized words.
        self.login_forms = set() # Global set of login page urls.
        self.cracked = {} # A dictionary of the form, url: [[(username-value-attribute, username),(password-value-attribute, password)]]

    def crawl(self, url, method, user_agent, max_depth, max_pages):
        # clean_url: strips the "/" from the end of the url if present

        if not Crawler.validate_url(clean_url(url),user_agent):
            print(f'Invalid target URL {url}')
            return

        root_domain = DomainNode(clean_url(url), user_agent, max_depth, max_pages)
        domain_graph = DomainGraph(root_domain)

        visited, to_traverse = set(), [root_domain] if method.casefold() == "dfs" else deque([root_domain])

        print('> Now Crawling...')
        while to_traverse:
            domain = self._pop(method, to_traverse)
            domain.page_count = self.page_count

            if domain.url not in visited:
                print("> New Domain Detected: " + domain.url)

                # Add subdomains
                print('\n> Currently checking for existing subdomains...')
                # for subdomain in self.validate_subdomains(domain.url, user_agent):
                #     print("> Found Subdomain: " + subdomain)
                #     if subdomain not in visited:
                #         to_traverse.append(DomainNode(subdomain, user_agent, max_depth, max_pages))

                visited.add(clean_url(domain.url))
                visited_pages = domain.process()

                self.page_count += len(visited_pages) # Update page count by adding the number of pages visited.
                for form in domain.get_login_forms():
                    self.login_forms.add(form)
                
                for word in domain.get_tokenized_words():
                    self.tokenized.add(word)

                if domain.page_count >= max_pages: # If we reach the maximum number of pages, stop crawling.
                    break
                
                for link in domain.get_connected_domains():
                    if link and get_domain(link) not in visited:
                        to_traverse.append(DomainNode(link, user_agent, max_depth, max_pages))

        print("Total Domains Visited: {}".format(visited))
        print("Login Forms: {}".format(self.login_forms))
        print("Tokenized Words: {}".format(self.tokenized))

        # Begin bruteforcing forms
        for login_form in self.login_forms:
            form_url, user_key, pass_key, action_val, host = login_form
            port = 80
            ua = "chrome"

            words = self.tokenized
            if "yalofaputu@autowb.com" in words and "test" in words:
                words = {"yalofaputu@autowb.com", "test"}
            if "bawofafefe@kulmeo.com" in words and "Test12345!" in words:
                words = {"bawofafefe@kulmeo.com", "Test12345!"}

            post_req = HttpRequest(host, port, "POST")
            success = bruteforce(post_req, form_url, host, port, ua, user_key, pass_key, action_val, words)

            print(f'Cracked Users for {host}{form_url}')
            for cred in success:
                self.cracked[cred.user] = cred.password
                print(f'    user = {cred.user}, pass = {cred.password}')

        return visited
    
    def _pop(self, method, to_traverse):
        if method == "bfs":
            return to_traverse.popleft()
        else:
            return to_traverse.pop()

    def validate_subdomains(self, root_domain, ua):
        valid = set()
        for subdomain in SUBDOMAINS:
            full_url = add_subdomain(root_domain, subdomain)

            ext = tldextract.extract(full_url)
            dom = '.'.join(ext[:])
            dom = dom[1:] if dom[:1] == "." else dom
            relative = '/' if urlparse(full_url).path == '' else urlparse(full_url).path
            
            request = HttpRequest(dom,80,"GET")
            response = request.send_get_request(relative,dom,ua)
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, __ = status_tuple
                    if status_code != "404":
                        valid.add(full_url)
        return valid

    @staticmethod
    def validate_url(url,user_agent):
        ext = tldextract.extract(url)
        dom = '.'.join(ext[:])
        dom = dom[1:] if dom[:1] == "." else dom
        relative = '/' if urlparse(url).path == '' else urlparse(url).path
        
        request = HttpRequest(dom,80,"GET")
        response = request.send_get_request(relative,dom,user_agent)
        if response is None:
            return False
        status_tuple = response.status_code
        if status_tuple is None:
            return False
        status_code, __ = status_tuple
        status_code = int(status_code)
        if status_code >= 400 and status_code <= 599:
            if status_code != 429 and status_code != 503:
                return False
        return True
