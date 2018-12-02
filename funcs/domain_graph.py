from collections import deque
import requests

import tokenize
from .page_graph import PageGraph

class DomainGraph:
    """ A custom graph data structure to store the family of a given root domain. """

    def __init__(self, root_domain):
        """ Constructs a new DomainGraph object.
        Parameters
        ----------
        root_domain : DomainNode
            the root domain node where a graph traversal will begin
        """
        self.root_domain = root_domain
    
    def __repr__(self):
        """ Returns a string representation of the DomainGraph class and its fields. """

        return 'DomainGraph(root_domain={})'.format(self.root)

    class DomainNode:
        
        # Eventually switch to passing in user_agent, max_pages, max_depth into a config and grab them from there.
        def __init__(self, url, user_agent, max_pages, max_depth):
            self.url = url
            self.user_agent = user_agent
            self.max_pages = max_pages
            self.max_depth = max_depth
            
            self.page_count = 0
            self.depths = { self.url: 0 }
            self.connected_domains = set()
            self.login_urls = set()
        
        def __repr__(self):
            return 'DomainNode(url={}, connected_domains={})'.format(self.url, self.connected_domains)
        
        def process(self):
            root_page = PageGraph.PageNode(self.url)
            page_graph = PageGraph(root_page)

            visited, queue = set(), deque([root_page])

            # Account for robots.txt later.
            # Maybe make a page node for each url in robots.txt and add it to the queue.

            while queue:
                current_page = queue.popleft()
                print("current page: " + current_page.url)

                if 200 >= requests.get(current_page.url).status_code <= 300:
                    self.page_count += 1
                
                if self.page_count == self.max_pages:
                    break
                
                if self.depths[current_page.url] >= self.max_depth:
                    break

                if current_page.url not in visited:
                    visited.add(current_page.url)
                    current_page.process() 

                    for link in current_page.get_connected_pages():
                        new_page_node = PageGraph.PageNode(link)
                        queue.append(new_page_node)

                        self.depths[link] = self.depths[current_page.url] + 1
                    
                    for link in current_page.get_other_domains():
                        self.connected_domains.add(link)
                    
                    for link in current_page.get_login_pages():
                        self.login_urls.add(link)
                        
        
        def get_connected_domains(self):
            return self.connected_domains

        def get_login_urls(self):
            return self.login_urls





