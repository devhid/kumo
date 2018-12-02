if __name__ = "__main__":
    url = "http://kumo.x10host.com"
    method = "dfs"
    agent = HTTP_UA_CHROME
    depth = 5
    pages = 10
    
    crawler = Crawler()
    crawler.crawl(url, method, agent, depth, pages)

def extract_path(url):
    return urllib.parse(full_url).path

def extract_hostname(url):
    extracted = tldextract.extract(url)
    return "{}.{}".format(extracted.domain, extracted.suffix)