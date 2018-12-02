<h1 align=center>kumo [クモ]</h1>
<h5 align=center>A kumo (クモ) is the japanese word for 'spider'.</h5>
<br>

## Overview
This project is an implementation of a **web crawler** and **form brute-forcer** that can "**autonomously navigate websites**, collecting and tokenizing all the words that it finds which it will later use as potential passwords on the website's login form". In addition, the crawler will "**autonomously identify the login page** and also detect whether a **combination of username and password was successful** or not".
  
## Installation
### 1. Clone this repository. 
```
git clone https://github.com/devhid/kumo && cd kumo
```

### 2. Install dependencies.
```
pip install .
```

- :zap: [Click](https://click.palletsprojects.com/en/7.x/) - A python package for creating beautiful command line interfaces.
- :globe_with_meridians: [TLDExtract](https://github.com/john-kurkowski/tldextract) - A url parsing library to easily extract domains and subdomains.
- :moneybag: [PyQuery](https://pythonhosted.org/pyquery/) - A python equivalent of JQuery.

