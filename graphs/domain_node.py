
from collections import deque

from graphs.page_graph import PageGraph
from graphs.page_node import PageNode
from utils.link_utils import get_domain, get_robot_links

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

import tldextract
from urllib.parse import urlparse

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
        self.login_forms = set()
        self.tokenized_words = set()

    def __repr__(self):
        return 'DomainNode(url={})'.format(self.url)

    def process(self):
        root_page = PageNode(self.url)
        page_graph = PageGraph(root_page)

        visited, queue = set(), deque([root_page])

        # Account for robots.txt.
        print("\n> Currently checking for valid links in robots.txt...")
        for robot_url in self.check_robots():
            print("> Found Robot Path: " + robot_url)
            robot_page = PageNode(robot_url)
            queue.append(robot_page)
            self.depths[robot_url] = 1

        while queue:
            current_page = queue.popleft()

            if current_page.url is not None and current_page.url not in visited:
                ext = tldextract.extract(current_page.url)
                dom = '.'.join(ext[:])
                dom = dom[1:] if dom[:1] == "." else dom
                relative = '/' if urlparse(current_page.url).path == '' else urlparse(current_page.url).path
                relative = relative.replace("\r","")
                request = HttpRequest(dom,80,"GET")
                response = request.send_get_request(relative,dom,self.user_agent)

                if response is None:
                    continue
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, __ = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        queue.append(current_page)
                    if status_code >= 400 and status_code <= 599:
                        continue
                else:
                    continue

                if status_code >= 200 and status_code <= 300:
                    print('------------------------------------------------------------')
                    print("> New Page: " + current_page.url)
                    visited.add(current_page.url)
                    current_page.process(self.user_agent) 

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
                            new_page_node = PageNode(link)
                            queue.append(new_page_node)
                            self.depths[link] = self.depths[current_page.url] + 1

                    for other_domain in current_page.get_other_domains():
                        self.connected_domains.add(other_domain)

                    for login_form in current_page.get_login_pages():
                        self.login_forms.add(login_form)
                    
                    for word in current_page.get_tokenized_words():
                        self.tokenized_words.add(word)
        
        print('------------------------------------------------------------')
        print("Pages Visited: {}".format(visited))
        print('------------------------------------------------------------\n')
        return visited
                    
    def get_tokenized_words(self):
        return self.tokenized_words

    def get_connected_domains(self):
        return self.connected_domains

    def get_login_forms(self):
        return self.login_forms

    def check_robots(self):
        domain = get_domain(self.url).replace("http://","")
        request = HttpRequest(domain,80,"GET")
        response = request.send_get_request("/robots.txt",domain,self.user_agent)

        if response is not None:
            if response.body is not None:
                return get_robot_links(response.body, self.url)
        return []