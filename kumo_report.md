<h1 align=center> kumo - the simple web brute-forcer </h1>

<h4 align=center> Mankirat Gulati, Andy Liang, Stanley Lim, Johnny So </h1>

This project is an implementation of a **web crawler** and **form brute-forcer** that can "**autonomously navigate websites**, collecting and tokenizing all the words that it finds which it will later use as potential passwords on the website's login form". In addition, the crawler will "**autonomously identify the login page** and also detect whether a **combination of username and password was successful** or not".



## Crawling the Web 

**kumo** starts at a specified target domain and builds its [graph model of the internet](#websites) as it analyzes web pages and traverses to the target's subdomains.

It is configured to use either [Breadth-First Search (BFS)](#Breadth-First-Search-BFS) or [Depth-First Search (DFS)](#Depth-First-Search-DFS) in its web-crawling, as either algorithm is guaranteed to visit every node exactly once in a connected component of the graph.

**kumo** _visits_ a page by sending an **HTTP GET** request and receiving the **HTTP response** sent back by the server. Then, it analyzes the HTML for links to other pages and domains. Depending on the crawling algorithm used (BFS or DFS), the links are processed differently. After the links are processed, **kumo** strips the HTML and tokenizes and transforms all the words (converts them to lowercase, uppercase, reverse and leet-speak) it can find and adds them to its database of words to use in brute-forcing the login forms.

After **kumo** is done with a page, it moves onto the next page according to specified graph traversal algorithm. However, regardless of whether it is BFS or DFS, since each domain (**not each page**) is its own vertex, it will **always** choose to visit another page in the same domain over a page in another domain. Only when **kumo** has detected that there are no other links to pages in the current domain does it choose to traverse to another domain using the specified graph traversal algorithm.

```html
<div style="page-break-after: always;"></div>
```

<h1 align=center> Table of Contents </h1>

1. [Functional Specifications](#Functional-Specifications)

   - [Prerequisites & Dependencies](#Prerequisites-&-Dependencies)
   - [Properties](#Properties)
   - [Technical Design](#Technical-Design)
   - 

2. [User Guide](#User-Guide)

   1. [Setup](#Setup)
   2. [Downloading](#Downloading)
   3. [Configs](#Configs)
   4. [How to Use](#How-To-Use)
   5. [Testing](#Testing)

3. [References](#References)

   1. [Internet Standards](#Internet-Standards)
   2. [Programming Guidelines](#Programming-Guidelines)

4. [Team Dynamics & Journey](#Team-Dynamics-&-Journey)

   1. [Workflow](#Workflow)
   2. [Brainstorming](#Brainstorming)
   3. [Feature Contributions](#Feature-Contributions)
   4. [Tying It Together](#Tying-It-Together)
   5. [Major Blockers](#Major-Blockers)
   6. [Presentation Planning](#Presentation-Planning)

   ```html
   <div style="page-break-after: always;"></div>
   ```


<h1 align=center> Functional Specifications </h1>

## Prerequisites & Dependencies

- :zap: [Click](https://click.palletsprojects.com/en/7.x/) - A python package for creating beautiful command line interfaces.
- :globe_with_meridians: [TLDExtract](https://github.com/john-kurkowski/tldextract) - A url parsing library to easily extract domains and subdomains.
- :moneybag: [PyQuery](https://pythonhosted.org/pyquery/) - A python equivalent of JQuery.



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

- ### Domain Graph

  A **kumo (クモ)** is the Japanese word for 'spider'; it is only fitting that the internet is thus represented as a graph. 

  #### Vertices

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

  #### Edges

  An edge from vertex `A` to vertex `B` exists if and only if at least one of the following holds:

  - there is a link on some webpage in domain `A` that goes to some webpage in domain `B`

  - vertex `B` is found from combining [this list of popular subdomains](https://github.com/rbsec/dnscan/blob/master/subdomains-100.txt) with the domain of `A`


- ### Page Graph

  #### Vertices

  Vertices in the **page graph** correspond to pages within a certain domain `D`. To completely process a domain `D`, **kumo** must crawl all the pages it can find under domain `D` before it can move onto a different domain `D'`.

  #### Edges

    An edge from vertex `A` to vertex `B` exists if and only if:

  - there is a link on webpage `A` to webpage `B`
  - webpage `A` is our root domain page and `B` is one of the links in `robots.txt`

- ### Tokenized Words

  Words are tokenized from a html body via the `PyQuery` library and stored inside a regular, global `set()`. As the crawler continues to traverse other pages, the set of tokenized words is updated with more words that are found.



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
      Accept-Encoding: 
      Accept-Charset: utf-8
      Connection: close
      \\r\\n\\r\\n
      ```

      **Uses**: `__send_request(self, url, protocol, host, agent, content_type, content_length, cache_control, accept, accept_lang, accept_encoding, accept_charset, connection, body)`

      **Returns**: `True` if the message was sent successfully, `False` otherwise

      **Note**: `Accept-Encoding` is blank because it would add unnecessary complexity. When receiving a response with the current socket, we cannot know how long the headers of the response will be. Thus we cannot know where the heading `Content-Encoding` will appear in order to read that value and apply the appropriate decoding(s). We could read up until we hit two consecutive newlines to get the headers and then read that for the `Content-Encoding` header, but it is left as a potential future improvement.

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
       Accept-Encoding: 
       Accept-Charset: utf-8
       Connection: close
       \\r\\n
       [body]
       \\r\\n\\r\\n
      ```

      **Uses**: `__send_request(self, url, protocol, host, agent, content_type, content_length, cache_control, accept, accept_lang, accept_encoding, accept_charset, connection, body)`
      **Returns**: `True` if the message was sent successfully, `False` otherwise

      **Note**: `Accept-Encoding` is blank because it would add unnecessary complexity. When receiving a response with the current socket, we cannot know how long the headers of the response will be. Thus we cannot know where the heading `Content-Encoding` will appear in order to read that value and apply the appropriate decoding(s). We could read up until we hit two consecutive newlines to get the headers and then read that for the `Content-Encoding` header, but it is left as a potential future improvement.

    - `generate_post_body(self, content_type, data)`

      Generates the HTTP body of a `POST` request given a `Content-Type` and `data`.

      **Returns**: the HTTP body of the `POST` request as a string (e.g. `key1=val1&key2=val2`)

      **Note**: only `Content-Type` of `application/x-www-form-urlencoded` is supported as `multipart/form-data` is used for uploading files which is unnecessary, and it is safe to assume `text/plain` is never used in a `POST` request.

  - **Static Methods**

    - `get_status_code(http_response)`

      Gets the HTTP status code from an HTTP response. Does basic validity checking on `http_response`.

      **Returns**: 

      - `None` if `http_response` is invalid

      - `(status_code, interesting_info)`

        If `status_code` is a redirect status code (of form `3xx`) then `interesting_info` is the preferred redirect URL. If there is no preferred redirect URL, `interesting_info` is `None`.

    - `get_body(http_response)`

      Gets the HTTP body from an HTTP response.

      **Returns**: the HTML body of the response or `None` if the response was not valid

      **Note**: the body begins after two consecutive newline characters in the response message. If two consecutive newline characters are not found, `http_response` was not valid. If there was no body, an empty string is returned.

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

  - `tokenize_html(html)`

    Retrieves all the words in the body section of a webpage's html document.

    **Uses:** tokenize_html(html)

    **Note:** Text in the body from JavaScript code and SVGs are not considered as valid words

- #### Text Transformation

  * **Transformation**
    The text transformation in **kumo** is included to encode or transform passwords in several different ways to simulate how some users would modify their passwords. The different transformations supported by **kumo**:
      * `lower` - converts given string to lowercase.
      * `upper` - converts given string to uppercase.
      * `reverse` - reverses given string.
      * `leet` - changes string with following changes:
        * 'a' -> '4'
        * 'e' -> '3'
        * 'l' -> '1'
        * 't' -> '7'
        * 'o' -> '0'

  ## transform.py
  `transform.py` is a module designed to store all the different versions of the strings as outlined above.

  - **Constructor**
    - `__init__(self, lower, upper, reverse, leet)`
        The constructor takes in the `lower`, `upper`, `reverse`, and `leet` version of a given string.

    - `__repr__(self)`
      Returns a string representation with all instance variables.

  - **Instance Variables**

    - `lower` - the lowercased version of the given word.
    - `upper` - the uppercased version of the given word.
    - `reverse` - the reversed version of the given word.
    - `leet` - the leet code version of a given word.

  - **Public**

    - `generate_transformations(strings)`

      Function designed to generate all the different transformations as listed above for the given list of strings, `strings`.

      **Uses**: `generate_transformations(strings)`

      **Returns**: A map where the word is the key and the transformation object as the value.

  - **Private**

    - `_generate_leet(string)`

      Generates the leet-speak version of a given string by performing the following **case-insensitive** replacements:

      - 'a' -> '4'
      - 'e' -> '3'
      - 'l' -> '1'
      - 't' -> '7'
      - 'o' -> '0'

      **Uses**: `_generate_leet(string)`

      **Returns**: Returns the leet-speak version of the string.


- #### Link Retrieval


  - `retrieve_links(html, base_url)`

    Retrieves all links in the webpage represented by the url.

    **Uses:** `retrieve_links(html, base_url)`

    **Returns:** Returns a set of all urls in the html

    **Note:** All relative urls are converted to absolute urls based off the provided `base_url`

- #### Detecting Login Forms

    - `detect_login(html, base_url)`

      Determine whether a login form is present in the webpage. If it is, identify its input names.

      **Uses:** `detect_login(html, base_url)`

      **Returns:** A namedtuple of the following form:

      ```Python
      namedtuple('Form', ['url', 'username', 'passname'])
      ```

      if a login form is found in the current webpage, `None` otherwise.

      - `url`: The action url that the form submits to. If none is provided, the input `base_url` is used instead.
      - `username`: The value of the name attribute in the username input tag. 
      - `passname`: The value of the name attribute in the password input tag.

  - **Detection Method** 

    **kumo** detects login forms by scanning the html document of each webpage, looking for a form with a `post` method. Within each of the form that it finds, it parses the input tags and analyzes all their attributes. The attribute values are compared with a predefined set of keywords to determine whether the input is a username/email input or a password input. Username inputs also typically require the attribute-value pair `type="text"` while password inputs typically require the attribute value pair `type="password"`. To distinguish login forms from register forms, **kumo** analyzes the submit portion of the form, looking through the attribute values and text for keywords within another predefined set that would indicate that the form's function is for login rather than for register.

- #### Brute-forcing



### 3. Future Improvements

- Support for HTTPS servers
- Support for the `Accept-Encoding` for messages sent using `HttpRequest.send_get_request` and `HttpRequest.send_post_request`

```html
<div style="page-break-after: always;"></div>
```

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

```html
<div style="page-break-after: always;"></div>
```

<h1 align=center>References</h1>

# Testing

The project itself comes with a local website along with deployed instances of **Wordpress**.
Note that these websites are *designed specifically* to be exploited by **kumo** rather than testing on other live websites.

## Local (Flask)

A small Flask project to mock a regular website with different types of input forms can be found in `fake-website` directory.
To run the project, ensure that Flask is installed.
Follow the setup guide found in `README.md` inside the `fake-website` directory.

## Wordpress

### Internet Standards

- #### HTTP

  - ##### Headers and Message Format

    - [RFC 2616: HTTP](https://tools.ietf.org/html/rfc2616#section-4.2)

- #### SMTP

  - ##### [Case-Insensitive Email Addresses StackOverflow Question](https://stackoverflow.com/questions/9807909/are-email-addresses-case-sensitive)

    - References [RFC 5321: SMTP, Section 2.3-11](https://tools.ietf.org/html/rfc5321#section-2.3.11)



### Programming Guidelines

- #### Socket Programming

    - [Python Socket Library Documentation](https://docs.python.org/3/library/socket.html)
    - [Python Socket Library Programming Guidelines](https://docs.python.org/3/howto/sockets.html)



  ```html
  <div style="page-break-after: always;"></div>
  ```

<h1 align=center>Team Dynamics & Journey</h1>

## Workflow

The first topic we decided before we began our project was how to structure our workflow. We decided that we could all just choose a feature or component we wanted to work on, create a feature branch on Git, work on it, and merge on completion. Overall, this type of workflow worked very well for this type of project.



## Brainstorming

#### Command Line Interface vs. Web Application

* We were first thinking about whether to control the crawler through a simple command line interface or through an online web application. We decided that we should just build a simple command line interface and build a web application version if we had extra time (we didn't).

#### Domain Vertices vs. Pages Vertices

* At first, we were stuck on how we wanted to design our graph. We had a choice between designating each page as a vertex or each domain as a vertex. Ultimately, we realized that we wanted both.

#### Testing the Crawler

* In order to actually test the crawler, we needed a test website. **Stanley** worked on creating a simple website with login forms using **Flask**, but we realized that we also needed another website that had subdomains. Thus, **Stanley** also created a separate website on **WordPress** to handle that case.


## Feature Contributions

#### Stanley Lim

* Worked on **text transformation**, created the **test websites** using Flask and Wordpress to help test live usage of the crawler, and helped out with **bruteforcing**.

#### Johnny So

* Worked on manually creating **http requests**, helped with **bruteforcing**, created most of this **report**, and helped design **graph traversal strategies**.

#### Mankirat Gulati

* Started implementing **command line interface**, helped design the **graph data structures**, combined other components to implement the **main crawling logic**.

#### Andy Liang

* Created essential utility functions to handle **tokenization**, **link sanitization**, **domain matching**, and **login detection**.


## Tying It Together



## Major Blockers

#### Request Limits

* When we attempted to bruteforce credentials, there was a plugin in place in **WordPress** that detected this type of action and blocked further bruteforcing attempts. In order to circumvent this, the initial deployment of Wordpress switched from x10Host to AWS and tests were run using a VPN when the host machine's IP was blacklisted. When these solutions failed, a check was added in **kumo** to handle 429 and 503 status codes, which were errors for **too many requests** and **service unavailable** respectively.

#### Testing Issues

* We had trouble testing our modules because of the way Python handles relative imports in conjunction with working in a virtual environment. 

#### Graph Design and Traversal Strategies

* Designing the graph and traversal strategies were a pain because we always thought of new edge cases, so we needed to be **very specific** on how we wanted our crawler to work. Thus, this designing phase took a lot of our time.



## Presentation Planning

