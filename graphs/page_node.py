import requests
from utils.link_utils import retrieve_links, in_domain, detect_login, dom_family, tokenize_html

class PageNode:

    def __init__(self, url):
        self.url = url
        self.connected_pages = set()
        self.login_pages = set()
        self.other_domains = set()
        self.tokenized_words = set()
    
    def process(self):
        response = requests.get(self.url)
        if 400 <= response.status_code >= 599:
            return

        all_links = retrieve_links(response.content, self.url)

        for link in all_links:
            response = requests.get(link)

            # Continue with the next link if there are errors.
            if response.status_code >= 400 and response.status_code <= 599:
                continue
            
            # Handle redirection by looking at the Location header.
            if response.status_code >= 301 and response.status_code <= 308:
                redirect_url = response['Location']

                if in_domain(self.url, redirect_url):

                    inner_response = requests.get(redirect_url)
                    if inner_response.status_code == 200 or inner_response.status_code == 300:
                        login_page = detect_login(inner_response.content.decode('utf-8'), redirect_url)
                        if login_page:
                            self.login_pages.add(login_page)

                        self.connected_pages.add(redirect_url)
                        self.tokenized_words.update(tokenize_html(inner_response.content))

            # Handle status 300 the same as 200.
            if response.status_code >= 200 and response.status_code <= 300:
                if in_domain(self.url, link):
                    login_page = detect_login(response.content.decode('utf-8'), link)
                    if login_page:
                        self.login_pages.add(login_page)

                    self.connected_pages.add(link)
                    self.tokenized_words.update(tokenize_html(response.content.decode('utf-8')))
                elif dom_family(self.url, link):
                    if link not in self.other_domains:
                        self.other_domains.add(link)
                else:
                    continue

    def get_tokenized_words(self):
        return self.tokenized_words

    def get_other_domains(self):
        return self.other_domains
    
    def get_connected_pages(self):
        return self.connected_pages
    
    def get_login_pages(self):
        return self.login_pages