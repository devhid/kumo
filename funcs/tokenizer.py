# dependency imports
from pyquery import PyQuery as pq

def tokenize_html(html, include_all):
    """Return all tokenized strings from an html document passed as a string

    Parameters
    ---
    html: string
        String represention of a page's html document
    include_all: boolean
        True: retrieve words from the entire html document
        False: retrieve words from only within the body section of the html document

    Returns
    ---
    wordset: set<string>
        Set containing all the words on the current page
    """
    old_html = html
    if not include_all:
        start = html.find("<!doctype html>")
        if(start == -1):
            start = html.find("<html")

        html = html[start:]

    try:
        d = pq(html)
    except:
        # Page was invalid somehow
        d = pq(old_html)
    d('svg').remove()
    d('script').remove()
    d('style').remove()
    wordset = set()

    if not include_all:
        sentences = d('body').text()
    else:
        sentences = d.text()

    for word in sentences.split():
        wordset.add(word)
    
    return wordset