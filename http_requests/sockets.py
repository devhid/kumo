# Python Imports
import socket
import sys

# utils Imports
from utils.constants import HTTP_UA

def connect(url, port):
    """ Creates and returns a socket that is connected to the specified URL.
    
    This socket should be used for only ONE transfer (one send & one receive).

    Parameters
    ----------
    url : string
        the URL that a socket will attempt to bind to
    port : int
        the port that the socket will attempt to bind to

    Returns
    -------
    clientSocket : socket, None
        the socket that is binded to the URL, or None if it could not be created
    """
    try:
        client_socket = socket.create_connection((url,port))
        return client_socket
    except socket.error as err:
        return None

def send(socket, msg):
    """ Sends a message to a socket.

    Parameters
    ----------
    socket : socket
        the socket describing a connection, created by connect(url,port)
    msg : string
        the message that is to be sent
    
    Returns
    -------
    total_sent : int
        number of bytes sent; should be len(msg) or 0 if msg failed to completely send
    """
    total_sent = 0

    if socket is None or msg is None:
        return total_sent

    while total_sent < len(msg):
        sent = socket.send(msg[total_sent:].encode())
        if sent == 0:
            return 0    # message failed to completely send
        total_sent += sent

    return total_sent

def receive(socket):
    """ Receives a message from a socket.

    It detects the end of the message when it receives 0 bytes, as each socket
    should only be used for one transfer.

    Parameters
    ----------
    socket : socket
        the socket describing a connection, created by connect(url,port)
    
    Returns
    -------
    response : string
        HTTP response received
    """
    response = ""

    if socket is None:
        return response

    while True:
        message = socket.recv(4096)
        if len(message) == 0:
            break
        response += message.decode()
    
    return response

def send_request(socket, method, url, protocol, host, agent, 
                 content_type, content_length, cache_control, accept, 
                 accept_lang, accept_encoding, accept_charset, connection):
    """ Sends an HTTP Request to the specified socket created by connect(url,port).

    Request is formatted as follows:
        [method] [url] [protocol]
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
    socket : socket
        the socket describing a connection, created by connect(url,port)
    method : string
        HTTP method to use in the request (supports GET & POST)
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

    Returns
    -------
    status : boolean
        True if the request was sent, False if not
    """
    if socket is None or method is None or url is None or \
        protocol is None or host is None or agent is None or \
        cache_control is None or accept is None or accept_lang is None or \
        accept_encoding is None or accept_charset is None or connection is None:
        return False
    if method != "GET" and method != "POST":
        return False
    if method == "GET" and cache_control is None or accept is None or \
        accept_lang is None or accept_encoding is None or \
        accept_charset is None or connection is None:
        return False
    if method == "POST" and content_type is None:
        return False
    
    user_agent = agent
    if user_agent in HTTP_UA:
        user_agent = HTTP_UA[user_agent]

    request = method + " " + url + " " + protocol + "\n"
    request += "Host: " + host + "\n"
    request += "User-Agent: " + user_agent + "\n"
    if content_type is not None:
        request += "Content-Type: " + content_type + "\n"
    if content_length is not None:
        request += "Content-Length: " + content_length + "\n"
    if cache_control is not None:
        request += "Cache-Control: " + cache_control + "\n"
    if accept is not None:
        request += "Accept: " + accept + "\n"
    if accept_lang is not None:
        request += "Accept-Language: " + accept_lang + "\n"
    if accept_encoding is not None:
        request += "Accept-Encoding: " + accept_encoding + "\n"
    if accept_charset is not None:
        request += "Accept-Charset: " + accept_charset + "\n"
    if connection is not None:
        request += "Connection: " + connection
    request += "\r\n\r\n"

    sent = send(socket,request)
    if sent > 0:
        return True
    return False

def send_get_request(socket, url, host, agent):
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
    socket : socket
        the socket describing a connection, created by connect(url,port)
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
    return send_request(socket=socket,
                        method="GET",
                        url=url,
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
                        connection="close")

def send_post_request(socket, url, host, agent, 
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
    socket : socket
        the socket describing a connection, created by connect(url,port)
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
    return send_request(socket=socket,
                        method="POST",
                        url=url,
                        protocol="HTTP/1.1",
                        host=host,
                        agent=agent,
                        content_type=content_type,
                        content_length=content_length,
                        cache_control=None,
                        accept=None,
                        accept_lang="en-US,en;q=0.9",
                        accept_encoding=None,
                        accept_charset="utf-8",
                        connection=None)

def generate_post_body(content_type, data):
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
    body = ""
    if content_type == "application/x-www-form-urlencoded":
        # Expect data to be a dictionary.
        for key in data:
            body += key + "=" + data[key] + "&"
    else:
        return None
    return body[:len(body)-1] if len(body) >= 1 else body

def close(mysocket):
    """ Closes the specified socket.

    Parameters
    ----------
    socket : socket
        the socket describing a connection, created by connect(url,port)
    """
    if mysocket is not None:
        mysocket.shutdown(socket.SHUT_RDWR)
        mysocket.close()
        mysocket = None
    

