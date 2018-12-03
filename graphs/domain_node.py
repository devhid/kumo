# dependency imports
import tldextract as tld

# python imports
from collections import deque
from urllib.parse import urlparse
import time

# graphs imports
from graphs.page_graph import PageGraph
from graphs.page_node import PageNode

# utils imports
from utils.constants import HTTP_PORT, HTTP_TOO_MANY_REQ
from utils.link_utils import get_domain, get_robot_links, clean_url, extract_host_rel

# network imports
from network.HttpRequest import HttpRequest
from network.HttpResponse import HttpResponse

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
        self.retries = {} # key = url of page that returned 429 or 503, value is # of tries

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
                response = HttpRequest.get(current_page.url, self.user_agent)

                if response is None:
                    continue
                status_tuple = response.status_code
                if status_tuple is not None:
                    status_code, redirect_url = status_tuple
                    status_code = int(status_code)
                    if status_code == 429 or status_code == 503:
                        self.retries[current_page.url] = 1 if current_page.url not in self.retries else self.retries[current_page.url] + 1
                        if self.retries[current_page.url] < HTTP_TOO_MANY_REQ:
                            queue.appendleft(current_page)
                            time.sleep(2)
                    if status_code >= 400 and status_code <= 599:
                        continue
                else:
                    continue

                if status_code >= 200 and status_code <= 300:
                    print('------------------------------------------------------------')
                    tld_ext = tld.extract(current_page.url)
                    ext = extract_host_rel(current_page.url)
                    url = "http://"+ clean_url(ext.host + ext.rel_url)
                    if url.replace("\r","") not in visited:
                        print("> New Page: " + current_page.url)
                        visited.add(url)
                        self.page_count += 1
                        print("Page Count: " + str(self.page_count))
                    else:
                        print("> Redirected Page: " + current_page.url)
                    current_page.process(self.user_agent) 
                    
                    print("Depth: " + str(self.depths[current_page.url]))

                    if current_page.is_login_page(ext.rel_url):
                        print("> Login Page Detected: " + current_page.url)
            
                    if self.depths[current_page.url] >= self.max_depth:
                        print("> Reached Max Depth: " + str(self.depths[current_page.url]))
                        break
            
                    if self.page_count == self.max_pages:
                        print("> Reached Max Page Count: " + str(self.page_count))
                        break
                    
                    for link in current_page.get_connected_pages():
                        link_ext = extract_host_rel(link)
                        link_url = "http://" + clean_url(link_ext.host + link_ext.rel_url)
                        if link_url not in visited:
                            new_page_node = PageNode(link_url)
                            queue.append(new_page_node)
                            self.depths[link_url] = self.depths[current_page.url] + 1

                    for other_domain in current_page.get_other_domains():
                        self.connected_domains.add(other_domain)

                    for login_form in current_page.get_login_pages():
                        self.login_forms.add(login_form)
                    
                    for word in current_page.get_tokenized_words():
                        self.tokenized_words.add(word)
                # if redirected, throw the PageNode back into the front of the deque
                elif redirect_url is not None:
                    self.depths[redirect_url] = self.depths[current_page.url]
                    visited.add(current_page.url)           # handle infinite redirect loops
                    self.depths.pop(current_page.url,None)
                    current_page.url = redirect_url
                    queue.appendleft(current_page)          # handle in the next loop
        
        print('------------------------------------------------------------')
        visited_list = list(visited)
        # if redirected to http:// when trying no schema or with \r at end
        visited_list = [clean_url(s).replace("\r","") for s in visited_list]
        visited = set(visited_list)
        print("Pages Visited: {}".format(visited))
        print(f"{len(visited)} pages.")
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
        request = HttpRequest(domain,HTTP_PORT,"GET")
        response = request.send_get_request("/robots.txt",domain,self.user_agent)

        if response is not None:
            if response.body is not None:
                return get_robot_links(response.body, self.url)
        return []