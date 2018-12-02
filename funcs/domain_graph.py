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
        def __init__(self, url, user_agent, max_depth, max_pages):
            self.url = url
            self.user_agent = user_agent
            self.max_pages = max_pages
            self.max_depth = max_depth
            
            self.page_count = 0
            self.depths = { self.url: 0 }
            self.connected_domains = set()
            self.login_urls = set()
            self.reached_max_depth = False

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

                if current_page.url not in visited:
                    if 200 >= requests.get(current_page.url).status_code <= 300:
                        print("current page: " + current_page.url)

                        if current_page.url in current_page.get_login_pages():
                            print("login page found: " + current_page.url)
                
                        print("depth: " + str(self.depths[current_page.url]))
                        if self.depths[current_page.url] >= self.max_depth:
                            print("reached max depth: " + str(self.depths[current_page.url]))
                            self.reached_max_depth = True
                            break
                            
                        self.page_count += 1
                        print("page count: " + str(self.page_count))
                
                        if self.page_count == self.max_pages:
                            print("reached max page count: " + str(self.page_count))
                            break

                        visited.add(current_page.url)
                        current_page.process() 

                        for link in current_page.get_connected_pages():
                            if link not in visited:
                                new_page_node = PageGraph.PageNode(link)
                                queue.append(new_page_node)
                                self.depths[link] = self.depths[current_page.url] + 1

                        for link in current_page.get_other_domains():
                            if link not in self.connected_domains:
                                self.connected_domains.add(link)
                        
                        for link in current_page.get_login_pages():
                            if link not in self.login_urls:
                                self.login_urls.add(link)
            
            print("page visited: {}".format(visited))
            return visited
                        
        
        def get_connected_domains(self):
            return self.connected_domains

        def get_login_urls(self):
            return self.login_urls





