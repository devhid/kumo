"""
" A custom graph data structure to store referencing links from a given root URL.
"""
class LinkGraph:

    """
    " Constructs a new LinkGraph object.
    " :arg root: Node
    " :return: LinkGraph
    """
    def __init__(self, root):
        self.root = root
    
    def __repr__(self):
        return 'LinkGraph(root={})'.format(self.root)
    
    """
    " A representation of a vertex for a LinkGraph which stores a URL. 
    """
    class Node:
        
        """
        " Constructs a new Node object.
        " :arg url: String
        " :return: Node
        """
        def __init__(self, url):
            self.url = url
            self.links = set()
        
        def __repr__(self):
            return 'Node(url={})'.format(self.url)
        
        """
        " Links this current node to a new node with a specified url.
        " :arg url: String
        " :return: None
        """
        def add_link(self, url):
            self.links.add(url)

