# python imports
import time

# network imports
from network.HttpResponse import HttpResponse
from network.Socket import Socket

# utils imports
from utils.constants import HTTP_UA, HTTP_CONTENTTYPE_FORMENCODED, \
                            HTTP_GET, HTTP_POST, HTTP_PORT, HTTP_TOO_MANY_REQ
from utils.namedtuples import StatusCode, RequestInfo
from utils.link_utils import extract_host_rel

class HttpRequest:
   
    """ A simple class representing either a GET or POST request. 
    
    Example Usage:
        request = HttpRequest(url,port,method)
        for i in range(num_req):
            response = request.send_get_request(url,host,agent)
            if response is not None:
                status_tuple = response.status_code
                if status_tuple is not None:
                    print(status_tuple)
                headers = response.headers
                if headers is not None:
                    print(status_tuple)
                body = response.body
                if body is not None:
                    print(body)
                response_str = response.response
                print(response_str)
    """

    def __init__(self, url, port, method):
        """ Initializes a new HttpRequest.

        The same HttpRequest object can be re-used for requests to the same (url,port) 
        with the same HTTP method by calling the connect() and close() methods.
        
        Parameters
        ----------
        url : string
            the url to establish a connection to
        port : string
            the port on which to establish a connection to the url
        method : string
            HTTP method to use in the request (supports GET & POST)
        """
        self.__socket = Socket(str(url),port)
        self.__method = str(method)
    
    # Connecting Functions

    def connect(self):
        """ Initializes the underlying Socket that represents the connection. """
        self.__socket.connect()

    def close(self):
        """ Closes the underlying Socket that represents the connection. """
        self.__socket.close()

    # General Sending/Receiving Functions

    def __receive(self):
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
        # Obtain instance variables
        socket = self.__socket
        method = self.__method

        # Basic validity checking
        if socket is None or method is None or url is None or \
            protocol is None or host is None or agent is None:
            return False
        if method != HTTP_GET and method != HTTP_POST:
            return False
        if method == HTTP_GET:
            if cache_control is None or accept is None or \
            accept_lang is None or accept_encoding is None or \
            accept_charset is None or connection is None:
                return False
            if body is not None:
                return False
        if method == HTTP_POST and content_type is None:
            return False
        
        # Check if the user-agent is a pre-defined one, 
        # and if so replace it by its value.
        user_agent = agent
        if user_agent in HTTP_UA:
            user_agent = HTTP_UA[user_agent]

        # Construct the HTTP request message.
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

        # If the HTTP method is POST, then append the body
        if method == HTTP_POST:
            request += body

        # Attempt to send the HTTP request.
        sent = socket.send(request)
        
        # Indicate success.
        if sent > 0:
            return True

        # Indicate the HTTP request faile to (completely) send.
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
        response : HttpResponse
            an HttpResponse object describing the response, or None
            if the GET request failed to send
        """
        # Ensure the instance of the HttpRequest was made for GET requests
        if self.__method != HTTP_GET:
            return False

        # Connect the HttpRequest
        self.connect()

        # Defer to __send_request and specify arguments
        sent = self.__send_request(url=url,
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
        if sent:
            http_response = self.__receive()
            self.close()
            if http_response is None:
                return None
            return HttpResponse(http_response)
        self.close()
        return None
        
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
        response : HttpResponse
            an HttpResponse object describing the response, or None
            if the POST request failed to send
        """
        # Ensure the instance of the HttpRequest was made for POST requests
        if self.__method != HTTP_POST:
            return False

        # Connect the HttpRequest
        self.connect()

        # Defer to __send_request and specify arguments
        sent = self.__send_request(url=url,
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
        if sent:
            http_response = self.__receive()
            self.close()
            if http_response is None:
                return None
            return HttpResponse(http_response)
        self.close()
        return None

    # Static Methods

    @staticmethod
    def generate_post_body(content_type, data):
        """ Generates the HTTP Body of a POST request given a Content-Type and data.

        Only a Content-Type of "application/x-www-form-urlencoded" is supported.

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
        # Initalize our return value.
        body = ""

        # Basic validity checking. 
        # Only "application/x-www-form-urlencoded" is supported.
        #       "multipart/form-data" is necessary for binary data or large payloads,
        #           both of which are unnecessary in brute-forcing login forms.
        if not isinstance(data,dict) or content_type != HTTP_CONTENTTYPE_FORMENCODED:
            return None

        # We have ensured that data is a dictionary.
        for key in data:
            body += key + "=" + data[key] + "&"
             
        # Strip the last & character if necessary.
        return body[:len(body)-1] if len(body) >= 1 else body
        
    @staticmethod
    def get(url, agent):
        """ A convenience wrapper that instantiates an HttpRequest of type HTTP_GET,
        sends the message, and returns the HttpResponse.

        Parameters
        ----------
        url : string
            URL to send the HttpRequest to
        agent : string
            user-agent that wil be used

        Returns
        -------
        http_response : HttpResponse or None
            HttpResponse describing the response or None on failure
        """
        request_info = extract_host_rel(url)
        request = HttpRequest(request_info.host,HTTP_PORT,HTTP_GET)
        response = request.send_get_request(request_info.rel_url,request_info.host,agent)
        if response is None:
            return None
        return response
            

            


