# http_requests Imports
from http_requests.Socket import Socket

# utils Imports
from utils.constants import HTTP_UA

class HttpRequest:
   
    """ A simple class representing either a GET or POST request. 
    
    Example Usage:
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
    """

    def __init__(self, url, port, method):
        """ Initializes a new HttpRequest.
        
        Parameters
        ----------
        url : string
            the url to establish a connection to
        port : string
            the port on which to establish a connection to the url
        method : string
            HTTP method to use in the request (supports GET & POST)
        """
        self.__socket = Socket(url,port)
        self.__method = method
    
    # Connecting Functions

    def connect(self):
        """ Initializes the underlying Socket that represents the connection. """
        self.__socket.connect()

    def close(self):
        """ Closes the underlying Socket that represents the connection. """
        self.__socket.close()

    # General Sending/Receiving Functions

    def receive(self):
        """ Receives a message from the underlying Socket. 
        
        Returns
        -------
        response : string
            HTTP response received
        """
        return self.__socket.recv()
    
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

            [body]

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
        socket = self.__socket
        method = self.__method
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
    
    # Sending GET/POST requests

    def send_get_request(self, url, host, agent):
        """ Sends an HTTP GET Request to the specified socket created by connect(url,port).

        Request is formatted as follows:
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
        if self.__method != "GET":
            return False
        return self.__send_request(url=url,
                            protocol="HTTP/1.1",
                            host=host,
                            agent=agent,
                            content_type=None,
                            content_length=None,
                            cache_control="max-age=0",
                            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            accept_lang="en-US,en;q=0.9,ja;q=0.8",
                            accept_encoding="",
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
            Accept: application/json;text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
            Accept-Language: en-US,en;q=0.9,ja;q=0.8"
            Accept-Encoding: 
            Accept-Charset: utf-8
            Connection: close
            \\r\\n
            [body]
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
        if self.__method != "POST":
            return False
        return self.__send_request(url=url,
                            protocol="HTTP/1.1",
                            host=host,
                            agent=agent,
                            content_type=content_type,
                            content_length=content_length,
                            cache_control=None,
                            accept="application/json;text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            accept_lang="en-US,en;q=0.9,ja;q=0.8",
                            accept_encoding="",
                            accept_charset="utf-8",
                            connection="close",
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
        if self.__method != "POST":
            return None
        if not isinstance(data,dict):
            return None
        body = ""
        if content_type == "application/x-www-form-urlencoded":
            # Expect data to be a dictionary.
            for key in data:
                body += key + "=" + data[key] + "&"
        elif content_type == "multipart/form-data":
            # Not suppported; this is for uploading files
            return None
        else:
            # Anything else is not supported
            return None 
        return body[:len(body)-1] if len(body) >= 1 else body

    # Static Methods

    @staticmethod
    def get_status_code(http_response):
        """ Gets the HTTP status code from an HTTP response. 
            Does basic validity checking on http_response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response

        Returns
        -------
        (status_code, interesting_info) or None : (int, depends) or None
            status_code is the HTTP status code, and interesting_info is
            not None only if status_code == '3xx' and a preferred redirect
            link is in the http_response
        """
        lines = http_response.split("\n")
        status_code = 0
        interesting_info = None
        find_interesting_info = False
        if len(lines) > 0:
            words = lines[0].split(" ")
            if len(words) >= 3:
                status_code = words[1]
                if len(status_code) != 3:
                    return None
                if status_code[:1] == "3":
                    # Extract the preferred redirect URL.
                    find_interesting_info = True
            else:
                return None
        else:
            return None
        if find_interesting_info:
            for line in lines:
                words = line.split(" ")
                if len(words) > 0 and words[0] == "Location:":
                    interesting_info = words[1]
        return (status_code,interesting_info)

    @staticmethod
    def get_body(http_response):
        """ Gets the body from an HTTP response.

        Parameters
        ----------
        http_response : string
            string representing an HTTP response

        Returns
        -------
        body : string or None
            HTML body of the HTTP response, or None if http_response is not valid
        """
        body = http_response

        # HTTP body must begin after 2 consecutive newlines
        carriage_return = body.find("\r\n\r\n") != -1
        if carriage_return:
            index = body.find("\r\n\r\n") + 4
        else:
            index = body.find("\n\n")
            if index == -1:
                # Not a valid HTTP response
                return None
            index += 2
        body = body[index:]
        return body
        
            


