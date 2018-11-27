from pyquery import PyQuery as pq
import re

"""
" Return all tokenized strings from an html document passed as a string
" :arg html: string
" :return: { array<string> }
"""
def tokenize_html(html):
    d = pq(html)

    ret = []

    sentences = d.text()

    for word in sentences.split():
      ret.append(word)
    
    return ret

"""
" Return all links from an html document passed as a string
" :arg html: string
" :return: { set<string> }
"""
def retrieve_links(html):
  d = pq(html)

  ret = set()
  for link in d('a'):
    ret.add(link.attrib['href'])

  return ret