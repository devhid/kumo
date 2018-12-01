from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.parse import urljoin
import re

""" 
Return all tokenized strings from an html document passed as a string

Parameters
---
html: string
    String represention of a page's html document

Returns
---
wordset: set<string>
    Set containing all the words on the current page
"""
def tokenize_html(html):
    d = pq(html)

    wordset = set()

    sentences = d.text()

    for word in sentences.split():
        wordset.add(word)
    
    return wordset

"""
Return all links from an html document passed as a string

Parameters
---
html: string
    String represention of a page's html document
base_url: string
    Url of the html document's webpage

Returns
---
wordset: set<string>
    Set containing all the links on the current page
    Relative urls are converted to absolute using the current url
"""
def retrieve_links(html, base_url):
  d = pq(html)

  wordset = set()
  for link in d('a'):
    url = link.attrib['href']
    parsed_link = urlparse(url)
    print(url)
    if(parsed_link.netloc == ""): # Relative link
        url = urljoin(base_url, url)

    if(url[len(url) - 1] == "/"):
        url = url[0:len(url) - 1]

    wordset.add(url)

  return wordset

"""
Return all links from an html document passed as a string

Parameters
---
html: string
    String represention of a page's html document
base_url: string
    Url of the html document's webpage

Returns
---
login: boolean
    Return whether the current page is a login 
"""

