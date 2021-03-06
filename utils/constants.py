# configs
CFG_FILE = "configs.ini"
CFG_VALS = ['user_agent','traversal','max_depth','max_total']
CFG_DEF = "DEFAULT"

# help messages
HELP_AGENT = 'A custom user-agent for use with each GET/POST request.'
HELP_SEARCH_METHOD = 'The search traversal method for crawling: bfs|dfs.'
HELP_MAX_DEPTH = 'The maximum depth of pages to crawl.'
HELP_MAX_PAGES = 'The maximum total number of crawled pages.'
HELP_URL = 'The url to start crawling at.'
HELP_CFGS = 'The config set to use.'

# network 
## pre-defined user-agents
HTTP_UA_FIREFOX = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
HTTP_UA_CHROME = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
HTTP_UA_OPERA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
HTTP_UA_SAFARI = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
HTTP_UA_IE = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
HTTP_UA_GOOGLEBOT = 'Googlebot/2.1 (+http://www.google.com/bot.html)'
HTTP_UA = {'firefox':HTTP_UA_FIREFOX,'chrome':HTTP_UA_CHROME,
            'opera':HTTP_UA_OPERA,'safari':HTTP_UA_SAFARI,
            'ie':HTTP_UA_IE,'googlebot':HTTP_UA_GOOGLEBOT}

## form-urlencoded constant
HTTP_CONTENTTYPE_FORMENCODED = "application/x-www-form-urlencoded"

## request constants
HTTP_HEADERS = "headers"
HTTP_BODY = "body"
HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PORT = 80

## if we receive a 429 or 503 status code HTTP_TOO_MANY_REQ times, then assume failure
HTTP_TOO_MANY_REQ = 10
HTTP_RETRY_TIME = 2

# login_utils
## keywords for login success detection
SUCCESS_KEYWORDS = set(["success", "logged in", "authenticated", "successfully", "logged", "/login/?authentication=success", "/success", "redirected", "automatically"]) # TODO: Might need to try to expand this list

## keywords for login page detection
USER_KEYWORDS = set(["log in", "login", "log", "user", "username", "user_login", "user login", "user_id", "user id", "email"])
PASS_KEYWORDS = set(["pwd", "passwd", "pass", "password"])
LOGIN_KEYWORDS = set(["log in", "login", "signin", "sign in"])
REGISTER_KEYWORDS = set(["register", "signup", "sign up"])

SUBDOMAINS = "www,mail,ftp,localhost,webmail,smtp,pop,ns1,webdisk,ns2,cpanel,whm,autodiscover,autoconfig,\
            m,imap,test,ns,blog,pop3,dev,www2,admin,forum,news,vpn,ns3,mail2,new,mysql,old,lists,support,\
            mobile,mx,static,docs,beta,shop,sql,secure,demo,cp,calendar,wiki,web,media,email,images,img,\
            www1,intranet,portal,video,sip,dns2,api,cdn,stats,dns1,ns4,www3,dns,search,staging,server,mx1,\
            chat,wap,my,svn,mail1,sites,proxy,ads,host,crm,cms,backup,mx2,lyncdiscover,info,apps,download,\
            remote,db,forums,store,relay,files,newsletter,app,live,owa,en,start,sms,office,exchange,ipv4".split(',')
