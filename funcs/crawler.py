from collections import deque
import requests

from .domain_graph import DomainGraph
from .link_utils import *

class Crawler:
    def __init__(self):
        self.tokenized = set()
        self.login_page_urls = set()
        self.page_count = 0
        self.visited_urls = set()

    # def crawl()
    #   start_domain = DomainNode(user_input)
    #   domain_graph = DomainGraph(start_domain)
    #   Q.enq(start_domain)
    #   while Q is not empty:
    #       current_domain_node = Q.deq()
    #       current_domain_node.process()
    #       for link in current_domain_node.other_domain_links:
    #           Q.enq(domain(link))

    # DomainNode
    # def process():
    #   start_page = PageNode(self.domain)
    #   page_graph = PageGraph(start_page)
    #   Q.enq(start_page)
    #   while Q is not empty:
    #       current_pg = Q.deq()
    #       current_pg.process()
    #       for link in current_pg.curr_domain_links:
    #           make PageNode, do smth with it
    #       for link in current_pg.other_domain_links:
    #           self.__other_domain_links.add(link)

    """
        1) Start at a domain D and clean it if necessary.
            - D is either user input domain or obtained from queue or stack (i.e. in F(D))
        2) Make a GET request to the root page of domain D and obtain the response.
        3) Check the HTTP status code using HttpRequest.get_status_code(response).
        4) Perform the following actions if the status code is not 2xx or not 300:
            - HTTP 3xx (except 300): 
                IF the Location URL listed is within F(D) OR the domain entered is the user input domain:
                    - Update the original domain D to the redirected one and continue to step 5.
                ELSE: (location URL is not within F(D) AND not user input domain)
                    - Do not add that link to the queue or stack of domains to traverse.
            - HTTP 4xx/5xx:
                IF the domain is the initial domain input by the user:
                    - Return with error message.
                ELSE:
                    - Do not enqueue/push this domain to the queue or stack, respectively.
        5) Make a GET request to domain/robots.txt
            IF the status code == 200:
                - Extract all of the relative paths and rebuild its absolute path.
                - Add the absolute path version to the set of links for that domain.
        6) Retrieve all links from that domain by performing a breadth-first-search traversal.
            Note: Keep in mind that we only traverse a depth of 'max_depth' and crawl 'max_pages'.

            IF the link is an absolute path:
                IF the link is not within the domain:
                    - Do not add it.
                ELSE:
                    - Send a GET request to that link.
                        IF the status code is 200/300:
                            - Add that link to the set of links for that domain.
                        ELSE IF the status code is 3xx (besides 300):
                            - Make a GET request to the URL located in the Location header.
                            - If the status code is 200/300, add that link to the set of links for that domain.
                        ELSE:
                            - Do not add that link. 
            ELSE:
                - Rebuild the absolute path using the relative path.
                - Send a GET request to the absolute path link.
                    IF the status code is 200/300:
                            - Add that link to the set of links for that domain.
                        ELSE IF the status code is 3xx (besides 300):
                            - Make a GET request to the URL located in the Location header.
                            - If the status code is 200/300, add that link to the set of links for that domain.
                        ELSE:
                            - Do not add that link.
        7) When we are done processing the links for a domain, then for each link, we:
            - Tokenize all the words in the HTTP response body for that link and update the set 'self.tokenized'.
            - Check if there is a login form on that page:
                IF one exists:
                    - Bruteforce the credentials with the current tokenized words.
                        IF a pair of credentials work:
                            - Insert an entry in the 'cracked' dictionary with the domain as the key and a set containing a tuple for the username and password.
                        ELSE:
                            - Continue bruteforcing until we run out of pairs.
        8) We continue this process for each domain that was enqueued or pushed.

    """
    def crawl(self, url, method, user_agent, max_depth, max_pages):
        url = clean_url(url)

        root_domain = DomainGraph.DomainNode(url, user_agent, max_depth, max_pages)
        domain_graph = DomainGraph(root_domain)

        visited, to_traverse = set(), [root_domain] if method.casefold() == "dfs" else deque([root_domain])

        while to_traverse:
            domain = self._pop(method, to_traverse)
            domain.page_count = self.page_count

            if domain.url not in visited:
                print("> New Domain Detected: " + domain.url)

                visited.add(clean_url(domain.url))
                visited_pages = domain.process()

                self.page_count = len(visited_pages)

                if domain.page_count >= max_pages or domain.reached_max_depth:
                    break
                
                for link in domain.get_connected_domains():
                    if link and get_domain(link) not in visited:
                        to_traverse.append(DomainGraph.DomainNode(link, user_agent, max_depth, max_pages))

        print("Total Domains Visited: {}".format(visited))
        return visited
    
    def _pop(self, method, to_traverse):
        if method == "bfs":
            return to_traverse.popleft()
        else:
            return to_traverse.pop()
