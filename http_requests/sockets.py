# Python Imports
import socket
import sys

# Connection Functions

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

# Sending and Receiving Functions

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

    It detects the end of the message when it receives 0 bytes (EOF).

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

