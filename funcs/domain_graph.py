from collections import deque
import requests

import tokenize
from .page_graph import PageGraph
from .link_utils import *

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

        def __repr__(self):
            return 'DomainNode(url={}, connected_domains={})'.format(self.url, self.connected_domains)

        def process(self):
            root_page = PageGraph.PageNode(self.url)
            page_graph = PageGraph(root_page)

            visited, queue = set(), deque([root_page])

            # Account for robots.txt.
            print("\n> Currently checking for valid links in robots.txt...")
            for robot_url in self.check_robots():
                print("> Found Robot Path: " + robot_url)
                robot_page = PageGraph.PageNode(robot_url)
                queue.append(robot_page)
                self.depths[robot_url] = 1

            while queue:
                current_page = queue.popleft()

                if current_page.url not in visited:
                    response = requests.get(current_page.url).status_code
                    if not response:
                        return

                    if 200 >= requests.get(current_page.url).status_code <= 300:
                        print('------------------------------------------------------------')
                        print("> New Page: " + current_page.url)
                        visited.add(current_page.url)
                        current_page.process() 

                        if current_page.url in current_page.get_login_pages():
                            print("> Login Page Detected: " + current_page.url)
                
                        print("Depth: " + str(self.depths[current_page.url]))
                        if self.depths[current_page.url] >= self.max_depth:
                            print("> Reached Max Depth: " + str(self.depths[current_page.url]))
                            break
                            
                        self.page_count += 1
                        print("Page Count: " + str(self.page_count))
                
                        if self.page_count == self.max_pages:
                            print("> Reached Max Page Count: " + str(self.page_count))
                            break
                        
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
            
            print('------------------------------------------------------------')
            print("Pages Visited: {}".format(visited))
            print('------------------------------------------------------------\n')
            return visited
                        
        def get_connected_domains(self):
            return self.connected_domains

        def get_login_urls(self):
            return self.login_urls

        def check_robots(self):
            domain = get_domain(self.url)
            response = requests.get(domain + "/robots.txt")

            if response:
                return get_robot_links(response.content, self.url)
            return []





