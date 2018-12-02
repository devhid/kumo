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

#### Domain Graph

A **kumo (クモ)** is the Japanese word for 'spider'; it is only fitting that the internet is thus represented as a graph. 

##### Vertices

Vertices in the graph correspond to domains. **kumo** considers subdomains and parent domains as separate domains in its model. By specification, **kumo** crawls only one target family of domains `F(D)` and does not crawl to a domain that is not in the target's family of domains. 

We define a family of domains over a target domain `D` to be the set `F(D) = {a | a is a subdomain of D or a is a parent domain of D}`. The root domain `D` is specified by the user, and only vertices corresponding to domains in `F(D)` are graphed and crawled.

- **Subdomains and Parent Domains**

  Now what does it mean for domain `A` to be a **subdomain** of domain `B`, or for `A` to be a **parent domain** of `B`? It is best explained with an example. Let us say the user enters the starting domain to be `c.b.a.com`, and we find links to the following domains on the pages on `c.b.a.com`:
  - `a.com`
  - `b.a.com`
  - `e.d.c.b.a.com`
  - `f.e.d.c.b.a.com`
  - `b.com`

  Then we define the following pairs `(d,p)` such that `p` is a **parent domain** of `d`:

  - `(c.b.a.com, a.com)`
  - `(c.b.a.com, b.a.com)`

  We define the following pairs `(d,s)` such that `s` is a **subdomain** of `d`:

  - `(c.b.a.com, e.d.c.b.a.com)`
  - `(c.b.a.com, f.e.d.c.b.a.com)`

  One other term that may come in handy is a **direct subdomain** which we shall define as `(d,direct)` such that `direct` is a **direct subdomain** of `d`:

  - `(a.com, b.a.com)`
  - `(b.a.com, c.b.a.com)`
  - `(e.d.c.b.a.com, f.e.d.c.b.a.com)`

  Hence, if `D = c.b.a.com`, then `F(D) = {a.com, b.a.com, e.d.c.b.a.com, f.e.d.c.b.a.com}`. Note that `b.com` is **not in** `F(D)`.

##### Edges

An edge from vertex `A` to vertex `B` exists if and only if at least one of the following holds:

+ there is a link on some webpage in domain `A` that goes to some webpage in domain `B`

+ vertex `B` is found from combining [this list of popular subdomains](https://github.com/rbsec/dnscan/blob/master/subdomains-100.txt) with the domain of `A`


#### Tokenized Words

Library.



### 2. Feature Implementation

- #### Breadth-First Search (BFS)

- #### Depth-First Search (DFS)

- #### Completely Processing the Current Domain

- #### HTTP Requests

  HTTP request functionality is built into the `HttpRequest` class. Client code should only need to use `HttpRequest` to send HTTP requests/receive HTTP responses, and should not have to interact with the lower-level implementation of the sockets interface. The custom sockets interface is built on top of the standard Python3 `socket` library.

  The sections below describe how the sockets and HTTP request interfaces are implemented in **kumo**. An [example usage of client code using `HttpRequest`](#example-usage-of-`httprequest`) can be found at the end of this section.

  ## Sockets

  Socket functionality is split into two: a Python module `sockets.py` using relevant socket functions from the standard Python3 library `socket`, and a wrapper `Socket.py` class that uses the custom-defined functions in `sockets.py`.

  ### sockets.py

  `sockets.py` is a module with basic socket functionality. It has the following functions:

  - `connect(url, port)`

    Creates and returns a standard `socket` object that is connected to the specified URL and port.

    **Returns**: a standard `socket` object (`socket`)

    **Exception**: return `None`

  - `close(mysocket)`

    Closes the specified socket.

    **Returns**: does not return

    **Note**: the argument here is named `mysocket` instead of `socket` because it must call the standard method `socket.close()`

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

  ### Socket.py

  `Socket.py` is a wrapper that uses OOP principles over the functions defined in `sockets.py` to create a wrapping `Socket`  class to be used later. The `Socket` class has the following properties:

  - **Constructor**

    - `__init__(self,url,port)`

      The constructor takes a `url` and `port` that describes the socket connection, and assigns the instance variables appropriately.

  - **Private Instance Variables**

    - `self.__url`

      The `url` that the socket will connect to

    - `self.__port`

      The `port` that the socket will connect to the `url` on

    - `self.__socket`

      The underlying standard `socket` object

  - **Instance Methods**

    - `connect(self)`

      The underlying socket (`self.__socket`) connects to the specified `url (self.__url)`and `port (self.__port)` assigned during its construction.

      **Uses**: `sockets.connect(url, port)`

      **Returns**: does not return

      **Note**: This implementation allows for the same `Socket` object to be reused for the same `(url,port)`, which makes sense to code that uses this class, as the `Socket` object then represents an object that is used to connect to a `(url,port)`.

    - `close(self)`

      The underlying socket (`self.__socket`) is closed.

      **Uses**: `sockets.close(mysocket)`

      **Returns**: does not return

    - `send(self, msg)`

      The message `msg` is sent to the underlying socket (`self.__socket`), and the amount of bytes sent is returned.

      **Uses**: `sockets.send(socket, msg)`

      **Returns**: number of bytes sent (`int`)

    - `recv(self)`

      Receives and returns the message received from the underlying socket (`self.__socket`).

      **Uses**: `sockets.receive(socket)`

      **Returns**: message received from the `Socket` (`string`)

  ## Requests

  HTTP request functionality is implemented in the `HttpRequest.py` class, and depends on the `Socket.py` class.

  ### HttpRequest.py

  `HttpRequest.py` is a class that contains a `Socket` and represents either a `GET` or `POST` request. It provides convenience methods for sending either request, and other miscellaneous HTTP request functionality as described below.

  An instance of an `HttpRequest` can be reused to perform multiple HTTP requests of the same type to a specified `url` and `port`, by calling `connect()`, sending/receiving a request, and then calling `close()`.

  - **Constructor**

    - `__init__(self, url, port, method)`

      Initializes the `HttpRequest` instance by constructing a `Socket` to the specified `url` and `port` and setting the specified `method`.

  - **Private Instance Variables**

    - `self.__socket`

      The underlying `Socket` that describes the connection.

    - `self.__method`

      The HTTP request method.

  - **Instance Methods**

    - `connect(self)`

      Initializes the underlying `Socket` (`self.__socket`) that represents the connection.

      **Uses**: `Socket.connect()`

      **Returns**: does not return

      **Note**: after instantiation, use `connect()` every time another HTTP request is to be sent

    - `close(self)`

      Closes the underlying `Socket` (`self.__socket`) that represents the connection.

      **Uses**: `Socket.close()`

      **Returns**: does not return

    - `receive(self)`

      Receives a message from the underlying `Socket` (`self.__socket`)  that represents the connection.

      **Uses**: `Socket.recv()`

      **Returns**: message received from the `Socket` (`string`)

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

      **Note**: this method is denoted private by convention because client code should use either `send_get_request` or `send_post_request`, and not this general method.

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

  ## Example Usage of `HttpRequest`

  An example usage of client code interacting with the `http_requests` module is shown below.

  ```python
  # example usage of client code using HttpRequest to send a GET request
  request = HttpRequest(url,port,method)
  for i in range(num_req):
      request.connect()
      successful = request.send_get_request(self, url, host, agent)
      if successful:
          response = request.receive()
          print(response)
          tuple_ = HttpRequest.get_status_code(response)
          if tuple_ is not None:
              status_code, redirect_url = tuple_
              print("status code %s" % (status_code))
              if status_code[:1] == "3":
                  if redirect_url is not None:
                      print("redirect url %s" % (redirect_url))
                  else:
                      print("status_code is 300 Multiple Choices. Redirect URLs are in body.")
      request.close()
  ```

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
