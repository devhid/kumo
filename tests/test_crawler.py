
HTTP_UA_CHROME = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

from funcs.crawler import Crawler

if __name__ == "__main__":
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