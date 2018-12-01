import re
class Transformation:

    def __init__(self, lower, upper, reverse, leet):
        self.lower = lower
        self.upper = upper
        self.reverse = reverse
        self.leet = leet

    def __repr__(self):
        return 'Transformation=(lower={}, upper={}, reverse={}, leet={})'.format(self.lower, self.upper, self.reverse, self.leet)

"""
" Generates all variants for each given string (uppercase, reverse, and leet-speak)
" :arg strings: string[]
" :return: { string, Transformation }
"""
def generate_transformations(strings):
    res = dict()

    for string in strings:
        lower = string.lower()
        upper = string.upper()
        reverse = string[::-1]
        leet = _generate_leet(string) 
        res[string] = Transformation(lower, upper, reverse, leet)
    
    return res

"""
" Creates leet encoded version of string
" :arg string: String
" :return: String
"""
def _generate_leet(string):
    leet = re.sub('[Aa]', '4', string)
    leet = re.sub('[Ee]', '3', leet)
    leet = re.sub('[Ll]', '1', leet)
    leet = re.sub('[Tt]', '7', leet)
    leet = re.sub('[oO]', '0', leet)
    return leet