import requests
from collections import deque

from utils.constants import SUBDOMAINS
from utils.link_utils import clean_url, get_domain, add_subdomain
from graphs.domain_graph import DomainGraph
from graphs.domain_node import DomainNode
from bruteforce.bruteforce import bruteforce


class Crawler:
    def __init__(self):
        self.page_count = 0 # Global page counter.
        self.tokenized = set() # Global set of tokenized words.
        self.login_forms = set() # Global set of login page urls.
        self.cracked = {} # A dictionary of the form, url: [[(username-value-attribute, username),(password-value-attribute, password)]]

    def crawl(self, url, method, user_agent, max_depth, max_pages):
        # clean_url: strips the "/" from the end of the url if present

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
                # for subdomain in self.validate_subdomains(domain.url):
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


        return visited
    
    def _pop(self, method, to_traverse):
        if method == "bfs":
            return to_traverse.popleft()
        else:
            return to_traverse.pop()

    def validate_subdomains(self, root_domain):
        valid = set()
        for subdomain in SUBDOMAINS:
            full_url = add_subdomain(root_domain, subdomain)
            
            if requests.get(full_url):
                valid.add(full_url)
        
        return valid
            