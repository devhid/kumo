from graphs.domain_node import DomainNode

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

        return 'DomainGraph(root_domain={})'.format(self.root_domain)





