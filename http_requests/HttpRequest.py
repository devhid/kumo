# http_requests Imports
from http_requests import Socket

# utils Imports
from utils.constants import HTTP_UA

class HttpRequest:
   
    """ A simple class representing either a GET or POST request. """

    def __init__(self, socket, method):
        """ Initializes a new HttpRequest.
        
        Parameters
        ----------
        socket : Socket
            the socket describing a connection, created by connect(url,port)
        method : string
            HTTP method to use in the request (supports GET & POST)
        """
        self.socket = socket
        self.method = method
    
    def __send_request(self, url, protocol, host, agent, 
                 content_type, content_length, cache_control, accept, 
                 accept_lang, accept_encoding, accept_charset, connection, body):
        """ Sends an HTTP Request to the specified socket created by connect(url,port).

        Request is formatted as follows:
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

        Parameters
        ----------
        url : string
            url to which the HTTP request will affect based on method
        protocol: string
            HTTP protocol that the request follows
        host : string
            HTTP Host header
        agent : string
            HTTP User-Agent header
        content_type : string
            HTTP Content-Type header
        content_length : string
            HTTP Content-Length header
        cache_control : string
            HTTP Cache-Control header
        accept : string
            Http Accept header
        accept_lang : string
            HTTP Accept-Language header
        accept_encoding : string
            HTTP Accept-Encoding header
        accept_charset : string
            HTTP Accept-Charset header
        connection : string
            HTTP Connection header
        body : string
            HTTP request body

        Returns
        -------
        status : boolean
            True if the request was sent, False if not
        """
        socket = self.socket
        method = self.method
        if socket is None or method is None or url is None or \
            protocol is None or host is None or agent is None:
            return False
        if method != "GET" and method != "POST":
            return False
        if method == "GET":
            if cache_control is None or accept is None or \
            accept_lang is None or accept_encoding is None or \
            accept_charset is None or connection is None:
                return False
            if body is not None:
                return False
        if method == "POST" and content_type is None:
            return False
        
        user_agent = agent
        if user_agent in HTTP_UA:
            user_agent = HTTP_UA[user_agent]

        request = method + " " + url + " " + protocol + "\r\n"
        request += "Host: " + host + "\r\n"
        request += "User-Agent: " + user_agent
        if content_type is not None:
            request += "\r\nContent-Type: " + content_type
        if content_length is not None:
            request += "\r\nContent-Length: " + str(content_length)
        if cache_control is not None:
            request += "\r\nCache-Control: " + cache_control
        if accept is not None:
            request += "\r\nAccept: " + accept
        if accept_lang is not None:
            request += "\r\nAccept-Language: " + accept_lang
        if accept_encoding is not None:
            request += "\r\nAccept-Encoding: " + accept_encoding
        if accept_charset is not None:
            request += "\r\nAccept-Charset: " + accept_charset
        if connection is not None:
            request += "\r\nConnection: " + connection
        request += "\r\n\r\n"
        if method == "POST":
            request += body

        sent = socket.send(request)
        if sent > 0:
            return True
        return False

    def send_get_request(self, url, host, agent):
        """ Sends an HTTP GET Request to the specified socket created by connect(url,port).

        Request is formatted as follows:
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

        Parameters
        ----------
        url : string
            url to which the HTTP request will affect based on method
        host : string
            HTTP Host header
        agent : string
            HTTP User-Agent header

        Returns
        -------
        status : boolean
            True if the request was sent, False if not
        """
        if self.method != "GET":
            return False
        return self.__send_request(url=url,
                            protocol="HTTP/1.1",
                            host=host,
                            agent=agent,
                            content_type=None,
                            content_length=None,
                            cache_control="max-age=0",
                            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            accept_lang="en-US,en;q=0.9",
                            accept_encoding="gzip, deflate, br",
                            accept_charset="utf-8",
                            connection="close",
                            body=None)
                            
    def send_post_request(self, url, host, agent, 
                        content_type, content_length, body):
        """ Sends an HTTP POST Request to the specified socket created by connect(url,port).

        Request is formatted as follows:
            POST [url] HTTP/1.1
            Host: [host]
            User-Agent: [agent]
            Content-Type: [content_type]
            Content-Length: [content_length]
            \\r\\n
            BODY
            \\r\\n\\r\\n

        Parameters
        ----------
        url : string
            url to which the HTTP request will affect based on method
        host : string
            HTTP Host header
        agent : string
            HTTP User-Agent header
        content_type : string
            HTTP Content-Type header
        content_length : string
            HTTP Content-Length header
        body : string
            HTTP body

        Returns
        -------
        status : boolean
            True if the request was sent, False if not
        """
        if self.method != "POST":
            return False
        return self.__send_request(url=url,
                            protocol="HTTP/1.1",
                            host=host,
                            agent=agent,
                            content_type=content_type,
                            content_length=content_length,
                            cache_control=None,
                            accept="appplication/json",
                            accept_lang="en-US,en;q=0.9",
                            accept_encoding=None,
                            accept_charset="utf-8",
                            connection=None,
                            body=body)

    def generate_post_body(self, content_type, data):
        """ Generates the HTTP Body of a POST request given a Content-Type and data.

        Parameters
        ----------
        content_type : string
            HTTP Content-Type header
        data : dictionary
            data to be formatted into the body of the POST request

        Returns
        -------
        body : string
            body of the HTTP POST request, or None if the Content-Type was invalid
        """
        if self.method != "POST":
            return None
        if not isinstance(data,dict):
            return None
        body = ""
        if content_type == "application/x-www-form-urlencoded":
            # Expect data to be a dictionary.
            for key in data:
                body += key + "=" + data[key] + "&"
        else:
            return None 
        return body[:len(body)-1] if len(body) >= 1 else body
