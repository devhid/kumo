# Help messages for all the configuration options.
help_agent = 'A custom user-agent for use with each GET/POST request.'
help_search_method = 'The search traversal method for crawling: bfs|dfs.'
help_max_depth = 'The maximum depth of pages to crawl.'
help_max_pages = 'The maximum total number of crawled pages.'

# Sets of keywords for login page detection
USER_KEYWORDS = set(["log in", "login", "log", "user", "username", "user_login", "user login", "user_id", "user id", "email"])
PASS_KEYWORDS = set(["passwd", "pass", "password"])
LOGIN_KEYWORDS = set(["log in", "login", "signin", "sign in"])
REGISTER_KEYWORDS = set(["register", "signup", "sign up"])