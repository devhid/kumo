from collections import deque

""" 
" Provides breadth-first-search and depth-first-search traversal on a LinkGraph. 
"""
class Traversal:

    def __init__(self, method, link_graph):
        self.method = method
        self.link_graph = link_graph
    
    def __repr__(self):
        return 'Traversal=(method={}, link_graph={})'.format(self.method, self.link_graph)

    """
    " Starts a depth-first-search or breadth-first-search traversal.
    " :return: None
    """ 
    def start(self):
        if self.method == "dfs":
            self.dfs()
        else:
            self.bfs()

    """
    " Returns the depth-first-search traversal from a root node.
    " :return: set()
    """
    def dfs(self):
        visited, stack = set(), [self.link_graph.root]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(node.links - visited)
        
        return visited
    
    """
    " Returns the breadth-first-search traversal from a root node.
    " :return: set()
    """
    def bfs(self):
        visited, queue = set(), deque(self.link_graph.root)

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                queue.extend(node.links - visited)
        
        return visited

