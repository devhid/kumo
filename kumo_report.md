# kumo - the simple web brute-forcer

### [names]

This project is an implementation of a **web crawler** and **form brute-forcer** that can "**autonomously navigate websites**, collecting and tokenizing all the words that it finds which it will later use as potential passwords on the website's login form". In addition, the crawler will "**autonomously identify the login page** and also detect whether a **combination of username and password was successful** or not".



## Crawling the Web 

**kumo** starts at a specified target domain and builds its graph model of the internet as it analyzes web pages and traverses to other domains.

It is configured to use either [Breadth-First Search (BFS) ](#Breadth-First Search (BFS))or [Depth-First Search (DFS)](#Depth-First Search (DFS)) in its web-crawling, as either algorithm is guaranteed to visit every node exactly once in a connected component of the graph.

**kumo** _visits_ a page by sending an **HTTP GET** request and receiving the **HTTP response** sent back by the server. Then, it analyzes the HTML for links to other pages and domains. Depending on the crawling algorithm used (BFS or DFS), the links are processed differently. After the links are processed, **kumo** strips the HTML and tokenizes and transforms all the words (converts them to lowercase, uppercase, reverse and leet-speak) it can find and adds them to its database of words to use in brute-forcing the login forms.

After **kumo** is done with a page, it moves onto the next page according to specified graph traversal algorithm. However, regardless of whether it is BFS or DFS, since each domain (**not each page**) is its own vertex, it will **always** choose to visit another page in the same domain over a page in another domain. Only when **kumo** has detected that there are no other links to pages in the current domain does it choose to traverse to another domain using the specified graph traversal algorithm.



<h1 align=center> Functional Specifications </h1>



## Prerequisites & Dependencies

[prereqs & dependencies]



## Properties

[configurable properties]



## Technical Design

### Data Structures

#### 1. Websites - Graph

A **kumo (クモ)** is the Japanese word for 'spider'; it is only fitting that the internet is thus represented as a graph. Vertices in the graph correspond to domains (**kumo** considers subdomains as separate domains in its model, and in this document **domains** will refer to both separate and subdomains), and there exists an edge from vertex *A* to vertex *B* if and only if there is a *way* to get from A to B.

A *way* from *A* to *B* exists if at least one of the following holds:
​    + there is a link on *A* that directs the user to *B*
​    + *B* is a subdomain of *A*

#### 2. Tokenized Words

Library.



### Implementation

#### 1. Breadth-First Search (BFS)



#### 2. Depth-First Search (DFS)



#### 3. Completely Processing the Current Domain



#### 4. HTTP Requests



#### 5. Tokenizing Words



#### 6. Text Transformation



#### 7. Detecting Login Forms



#### 8. Bruteforcing



### Features



### Future Improvements



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