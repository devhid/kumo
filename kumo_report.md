# kumo - the simple web brute-forcer

### Mikey Gulati, Andy Liang, Stanley Lim, Johnny So

This project is an implementation of a **web crawler** and **form brute-forcer** that can "**autonomously navigate websites**, collecting and tokenizing all the words that it finds which it will later use as potential passwords on the website's login form". In addition, the crawler will "**autonomously identify the login page** and also detect whether a **combination of username and password was successful** or not".



## Crawling the Web 

**kumo** starts at a specified target domain and builds its [graph model of the internet](#websites) as it analyzes web pages and traverses to the target's subdomains.

It is configured to use either [Breadth-First Search (BFS)](#Breadth-First-Search-BFS) or [Depth-First Search (DFS)](#Depth-First-Search-DFS) in its web-crawling, as either algorithm is guaranteed to visit every node exactly once in a connected component of the graph.

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
  |    `bfs`    | [Breadth-First Search (BFS)](#Breadth-First-Search-BFS) |
  |    `dfs`    |   [Depth-First Search (DFS)](#Depth-First-Search-DFS)   |

- `max_depth` : `int > 0`

  The user can specify the maximum depth of pages to crawl with this value.

- `max_total` : `int > 0`

  The user can specify the maximum total number of crawled pages with this value.

## Technical Design

### 1. Data Structures

#### Websites

A **kumo (クモ)** is the Japanese word for 'spider'; it is only fitting that the internet is thus represented as a graph. Vertices in the graph correspond to domains (**kumo** considers subdomains as separate domains in its model. **kumo**, by specification, crawls only one website and does not crawl to a domain that is different from the target), and there exists an edge from vertex *A* to vertex *B* if and only if there is a *way* to get from *A* to *B*.

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

  - #### Sockets

    Socket functionality is split into two: a Python module `sockets.py` using relevant socket functions from the standard Python3 library `socket`, and a wrapper `Socket.py` class that uses the custom-defined functions in `sockets.py`.

    ## sockets.py

    `sockets.py` is a module with basic socket functionality. It has the following functions:

    - `connect(url, port)`

      Creates and returns a standard `socket` object that is connected to the specified URL and port.

      **Returns**: a standard `socket` object (`socket`)

      **Exception**: return `None`

    - `send(socket, msg)`

      Sends a message to a socket. Returns the number of bytes sent.

      **Returns**: number of bytes sent (`int`)

      **Exception**: return `0` if either argument was `None` or if the message failed to completely send.

      **Note**: The message fails to completely send if the socket is closed on the other (receiving) end before the message sends, amongst other reasons.

    - `receive(socket)`

      Receives and returns a message from a socket. It detects the end of the message when it reads that the length read was `0` bytes, indicating `EOF`.

      **Returns**: message received from the socket (`string`)

      **Exception**: return `""` (empty string) if `socket` is `None`

      **Note**: The reason it is implemented in such a way is that it is impossible to determine the length of the message unless a prior format is agreed to between the sender and receiver. Since **kumo** is designed to work on any general website, this method cannot be used, and **kumo** must rely on this method of checking.

    - `close(mysocket)`

      Closes the specified socket, and then assigns `mysocket` to be `None`.

      **Returns**: does not return

      **Note**: the argument here is named `mysocket` instead of `socket` because it must call the standard method `socket.close()`

    ## Socket.py

    `Socket.py` is a wrapper that uses OOP principles over the functions defined in `sockets.py` to create a wrapping `Socket`  class to be used later. The `Socket` class has the following properties:

    - **Constructor**

      - `__init__(self,url,port)`

        The constructor takes a `url` and `port` that describes the socket connection, and assigns the instance variables appropriately.

    - **Instance Variables**

      - `url` - the `url` that the socket will connect to
      - `port` - the `port` that the socket will connect to the `url` on
      - `socket` - the underlying standard `socket` object

    - **Instance Methods**

      - `connect(self)`

        The underlying socket (`self.socket`) connects to the specified `url (self.url)`and `port (self.port)` assigned during its construction.

        **Uses**: `sockets.connect(url, port)`

        **Returns**: does not return

        **Note**: This implementation allows for the same `Socket` object to be reused for the same `(url,port)`, which makes sense to code that uses this class, as the `Socket` object then represents an object that is used to connect to a `(url,port)`.

      - `close(self)`

        The underlying socket (`self.socket`) is closed.

        **Uses**: `sockets.close(mysocket)`

        **Returns**: does not return

      - `send(self, msg)`

        The message `msg` is sent to the underlying socket (`self.socket`), and the amount of bytes sent is returned.

        **Uses**: `sockets.send(socket, msg)`

        **Returns**: number of bytes sent (`int`)

      - `recv(self)`

        Receives and returns the message received from the underlying socket (`self.socket`).

        **Uses**: `sockets.receive(socket)`

        **Returns**: message received from the socket (`string`)

  - #### Requests

    HTTP request functionality is implemented in the `HttpRequest.py` class, and depends on the `Socket.py` class.

    ## HttpRequest.py

    `HttpRequest.py` is a class that contains a `Socket` and represents either a `GET` or `POST` request. It provides convenience methods for sending either request, and other miscellaneous HTTP request functionality as described below.

    - **Constructor**

      - `__init__(self, socket, method)`

    - **Instance Variables**

      - `self.socket`
      - `self.method`

    - **Instance Methods**

      - **Private**

        - `__send_request(self, url, protocol, host, agent, content_type, content_length, cache_control, accept, accept_lang, accept_encoding, accept_charset, connection, body)`

          A generic method for sending an HTTP `GET` or `POST` request. The arguments describe header values for the request. It is formatted as follows:

          ```
          [self.method] [url] [protocol]
          Host: [host]
          User-Agent: [agent]
          Cache-Control: [cache-control]
          Accept: [accept]
          Accept-Language: [accept-lang]
          Accept-Encoding: [accept-encoding]
          Accept-Charset: [accept-charset]
          Connection: [connection]
          \\r\\n\\r\\n
          
          [body]
          ```

          **Uses**: `Socket.send(msg)`

          **Returns**: `True` if the message was sent successfully, `False` otherwise

      - **Public**

        - `send_get_request(self, url, host, agent)`

          Sends an HTTP `GET` request to the specified `socket` (`self.socket`).

          The `GET` request is formatted as follows:

          ```
          GET [url] HTTP/1.1
          Host: [host]
          User-Agent: [agent]
          Cache-Control: max-age=0
          Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
          Accept-Language: en-US,en;q=0.9
          Accept-Encoding: gzip, deflate, br
          Accept-Charset: utf-8
          Connection: close
          \\r\\n\\r\\n
          ```

          **Uses**: `__send_request(self, url, protocol, host, agent, content_type, content_length, cache_control, accept, accept_lang, accept_encoding, accept_charset, connection, body)`

          **Returns**: `True` if the message was sent successfully, `False` otherwise

        - `send_post_request(self, url, host, agent, content_type, content_length, body)`

          Sends an HTTP `POST` request to the specified `socket` (`self.socket`).

          The `POST` request is formatted as follows:

          ```
           POST [url] HTTP/1.1
           Host: [host]
           User-Agent: [agent]
           Content-Type: [content_type]
           Content-Length: [content_length]
           Accept: application/json;text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*; q=0.8
           Accept-Language: en-US,en;q=0.9,ja;q=0.8"
           Accept-Encoding: gzip, deflate, br
           Accept-Charset: utf-8
           Connection: close
           \\r\\n
           [body]
           \\r\\n\\r\\n
          ```

          **Uses**: `__send_request(self, url, protocol, host, agent, content_type, content_length, cache_control, accept, accept_lang, accept_encoding, accept_charset, connection, body)`

          **Returns**: `True` if the message was sent successfully, `False` otherwise

        - `generate_post_body(self, content_type, data)`

          Generates the HTTP body of a `POST` request given a `Content-Type` and `data`.

          **Returns**: the HTTP body of the `POST` request as a string 

          ​		(e.g. `key1=val1&key2=val2`)

          **Note**: only `Content-Type` of `application/x-www-form-urlencoded` is supported as `multipart/form-data` is used for uploading files which is unnecessary, and it is safe to assume `text/plain` is never used in a `POST` request.

    - **Static Methods**

      - `get_status_code(http_response)`

        Gets the HTTP status code from an HTTP response. Does basic validity checking on `http_response`.

        **Returns**: 

        - `None` if `http_response` is invalid

        - `(status_code, interesting_info)`

          If `status_code` is a redirect status code (of form `3xx`) then `interesting_info` is the preferred redirect URL. If there is no preferred redirect URL, `interesting_info` is `None`.

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
