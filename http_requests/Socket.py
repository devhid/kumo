from http_requests import sockets

class Socket:
    
    """ A simple Socket class wrapping functionality from the http_requests/sockets module. """

    def __init__(self,url,port):
        """ Initializes a new Socket. This Socket should represent a connection to the (url,port).

        The same Socket object can be re-used for connections to the same (url,port) by calling
        the connect() and close() methods.

        Parameters
        ----------
        url : string
            the url to establish a connection to
        port : string
            the port on which to establish a connection to the url
        """
        self.__url = url
        self.__port = port
        
    # Connection Functions

    def connect(self):
        """ Establishes the connection to the specified url and port given during construction. """
        self.__socket = sockets.connect(self.__url,self.__port)

    def close(self):
        """ Closes the connection to the specified url and port given during construction. """
        sockets.close(self.__socket)

    # Sending and Receiving Functions

    def send(self, msg):
        """ Sends a message into the connection described by the underlying socket.

        Parameters
        ----------
        msg : string
            message to send into the connection

        Returns
        -------
        total_sent : int
            number of bytes sent; should be len(msg) or 0 if msg failed to completely send
        """
        return sockets.send(self.__socket,msg)

    def recv(self):
        """ Receives a message from the underlying socket.

        It detects the end of the message when it receives 0 bytes, as each Socket
        should only be used for one transfer.
        
        Returns
        -------
        response : string
            HTTP response received
        """
        return sockets.receive(self.__socket)