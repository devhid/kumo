import requests

class PageGraph:

    def __init__(self, root_page):
        self.root_page = root_page

    class PageNode:

        def __init__(self, url):
            self.url = url
            self.connected_pages = set()
            self.login_pages = set()
            self.other_domains = set()
        
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
                            if detect_login(inner_response.content):
                                self.login_pages.add(redirect_url)

                            self.connected_pages.add(redirect_url)

                # Handle status 300 the same as 200.
                if response.status_code >= 200 and response.status_code <= 300:
                    if in_domain(self.url, link):
                        if detect_login(response.content, link):
                            self.login_pages.add(link)

                        self.connected_pages.add(link)
                    else:
                        self.other_domains.add(link)

        def get_other_domains(self):
            return self.other_domains
        
        def get_connected_pages(self):
            return self.connected_pages
        
        def get_login_pages(self):
            return self.login_pages

"""
            # url = self.url
            # port = 80
            # method = "GET"
            # host = tokenize.extract_host(url)
            # pathname = tokenize.extract_path(url)

            # request = HttpRequest(url, port, method)
            # for link in all_links:
            #     request.connect()
            #     successful = request.send_get_request(self, pathname, host, user_agent)

            #     if successful:
            #         response = request.receive()
            #         status = HttpRequest.get_status_code(response)

            #         if status:
            #             status_code, redirect_url = status
                
            #     request.close()
"""


            
