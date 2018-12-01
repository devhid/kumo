# kumo - the simple web brute-forcer

### Mankirat Gulati, Andy Liang, Stanley Lim, Johnny So

This project is an implementation of a **web crawler** and **form brute-forcer** that can "**autonomously navigate websites**, collecting and tokenizing all the words that it finds which it will later use as potential passwords on the website's login form". In addition, the crawler will "**autonomously identify the login page** and also detect whether a **combination of username and password was successful** or not".



## Crawling the Web 

**kumo** starts at a specified target domain and builds its [graph model of the internet](#websites) as it analyzes web pages and traverses to the target's subdomains.

It is configured to use either [Breadth-First Search (BFS)](#Breadth-First Search-(BFS)) or [Depth-First Search (DFS)](#Depth-First Search-(DFS)) in its web-crawling, as either algorithm is guaranteed to visit every node exactly once in a connected component of the graph.

**kumo** _visits_ a page by sending an **HTTP GET** request and receiving the **HTTP response** sent back by the server. Then, it analyzes the HTML for links to other pages and domains. Depending on the crawling algorithm used (BFS or DFS), the links are processed differently. After the links are processed, **kumo** strips the HTML and tokenizes and transforms all the words (converts them to lowercase, uppercase, reverse and leet-speak) it can find and adds them to its database of words to use in brute-forcing the login forms.

After **kumo** is done with a page, it moves onto the next page according to specified graph traversal algorithm. However, regardless of whether it is BFS or DFS, since each domain (**not each page**) is its own vertex, it will **always** choose to visit another page in the same domain over a page in another domain. Only when **kumo** has detected that there are no other links to pages in the current domain does it choose to traverse to another domain using the specified graph traversal algorithm.



<h1 align=center> Functional Specifications </h1>



## Prerequisites & Dependencies

- :zap: [Click](https://click.palletsprojects.com/en/7.x/) - A python package for creating beautiful command line interfaces.



## Properties

The main configurable properties of **kumo** can be found in `/configs.ini`. An example of a valid `configs.ini` file is shown below:

### configs.ini

```ini
# /configs.ini

[BFS]
user_agent = chrome
traversal = bfs
max_depth = 10
max_total = 100

[DFS]
user_agent = chrome
traversal = dfs
max_depth = 10
max_total = 100
```

- `user_agent` : `string`

  The user can provide a custom user-agent that will be used by **kumo** in its HTTP requests, or use a pre-defined user-agent. The table below shows valid pre-defined `user_agent` values.

  | `user_agent` |               User-Agent Specified in Requests               |
  | :----------: | :----------------------------------------------------------: |
  |  `[Custom]`  |                          `[Custom]`                          |
  |  `firefox`   | `Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0` |
  |   `chrome`   | `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36` |
  |   `opera`    | `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41` |
  |   `safari`   | `Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1` |
  |     `ie`     | `Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)` |
  | `googlebot`  |      `Googlebot/2.1 (+http://www.google.com/bot.html)`       |

- `traversal` : `string`

  The user can specify what type of traversal **kumo** will use in crawling the interwebs. The table below shows valid `traversal` values.

  | `traversal` |                      Traversal Used                       |
  | :---------: | :-------------------------------------------------------: |
  |    `bfs`    | [Breadth-First Search (BFS)](#Breadth-First Search-(BFS)) |
  |    `dfs`    |   [Depth-First Search (DFS)](#Depth-First Search-(DFS))   |

- `max_depth` : `int > 0`

  The user can specify the maximum depth of pages to crawl with this value.

- `max_total` : `int > 0`

  The user can specify the maximum total number of crawled pages with this value.

## Technical Design

### 1. Data Structures

#### Websites

A **kumo (クモ)** is the Japanese word for 'spider'; it is only fitting that the internet is thus represented as a graph. Vertices in the graph correspond to domains (**kumo** considers subdomains as separate domains in its model, and in this document **domains** will refer to **only** subdomain. **kumo**, by specification, crawls only one website and does not crawl to a domain that is different from the target), and there exists an edge from vertex *A* to vertex *B* if and only if there is a *way* to get from *A* to *B*.

A *way* from *A* to *B* exists if at least one of the following holds:

+ there is a link on *A* that directs the user to *B* and *B* is a **direct** subdomain of *A*
+ *B* is a **direct** subdomain of *A*

Now what is a **direct** subdomain? It is best explained with an example. Say we have these domains:

- `a.com`
- `b.a.com`
- `c.b.a.com`
- `d.a.com`

We denote *only* these pairs `(a,b)` such that `a` is a **direct** subdomain of **b** (and hence, there exists an edge from `a` to `b` in the graph):

- `(b.a.com, a.com)`
- `(d.a.com, a.com)`
- `(c.b.a.com, b.a.com)`

Hence, although `c.b.a.com` is undoubtedly a subdomain of `a.com`, it is **not a direct subdomain** of `a.com` and there is no edge between the two in the graph modeled by **kumo**.

#### Tokenized Words

Library.



### 2. Feature Implementation

- #### Breadth-First Search (BFS)

- #### Depth-First Search (DFS)

- #### Completely Processing the Current Domain

- #### HTTP Requests

- #### Tokenizing Words

- #### Text Transformation

- #### Detecting Login Forms

- #### Bruteforcing



### 3. Future Improvements

- Support for HTTPS servers

<h1 align=center> User Guide </h1>

# Setup

This section of the report describes how **kumo** is set up to be deployed.

## Downloading

### Cloning via GitHub

Via SSH:

​	```git clone git@github.com:devhid/kumo.git```

Via HTTPS:

​	```git clone https://github.com/devhid/kumo.git	```

### Extracting ZIP



## Configs

This section of the report describes how **kumo** is configured. 

Refer to [Properties](#Properties) for an explanation of the main configurations.



# How to Use

This section of the report describes how to use **kumo** after it is [Setup](#Setup).



<h1 align=center>References</h1>

# Overall Guides

# Feature Implementation

### HTTP Requests

  + [Python Socket Library Documentation](https://docs.python.org/3/library/socket.html)
  + [Python Socket Library Programming Guidelines](https://docs.python.org/3/howto/sockets.html)
  + 



<h1 align=center>Team Dynamics & Journey</h1>

[Talk about initial splitting, meeting, brainstorming. Include design decisions.]

[Talk about each person's implementation of each feature.]

[Talk about tying it together.]

[Talk about major blockers.]

[Talk about presentation planning.]