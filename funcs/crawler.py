from collections import deque
from enum import Enum
import requests

from .tokenizer import tokenize_html, retrieve_links
from ..utils import file_utils
import .link_graph
 
SUBDOMAIN_FILE_PATH = '../subdomains.txt'

class Crawler:

    class TraversalMethod(Enum):
        BFS = 1,
        DFS = 2

    def crawl(self, root_domain, method):
        root = LinkGraph.Node(root_domain)
        visited, to_traverse = set(), [root] if method == TraversalMethod.BFS else deque(root)

        while to_traverse:
            domain = _pop(method, to_traverse)

            response = requests.get(domain)
            if response.status_code != 200:
                continue

            if domain not in visited:
                visited.add(domain)

                all_links = self._get_links(domain, to_traverse, response.content)
                domain.links = all_links
        
        return visited
    
    def _pop(self, method, to_traverse):
        if method == TraversalMethod.DFS:
            return to_traverse.popleft()
        else:
            return to_traverse.pop()
    
    def _get_links(self, domain, to_traverse, html):
        visited, queue = set(), deque(retrieve_links(links))

        while queue:
            link = queue.popleft()
            if link not in visited:
                visited.add(link)

                response = requests.get(link)
                if response.status_code != 200:
                    continue

                connected = retrieve_links(response.content)
                for clink in connected:
                    if within_domain(domain, clink) and clink not in visited:
                        queue.append(clink)
                    else:
                        self.to_traverse.append(clink)
        
        return visited





