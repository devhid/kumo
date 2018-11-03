class Transformations:

    def __init__(self, upper, reverse, leet):
        self.upper = upper
        self.reverse = reverse
        self.leet = leet

    def __repr__(self):
        return 'Transformation=(upper={}, reverse={}, leet={})'.format(self.upper, self.reverse, self.leet)

"""
" Generates all variants for each given string (uppercase, reverse, and leet-speak)
" :arg strings: string[]
" :return: { string, Transformations }
"""
def generate_transformations(strings):
    pass