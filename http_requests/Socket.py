from http_requests import sockets

class Socket:
    
    """ A simple Socket class wrapping functionality from the http_requests/sockets module. """

    def __init__(self,url,port):
        self.url = url
        self.port = port
        
    def connect(self):
        self.socket = sockets.connect(self.url,self.port)

    def close(self):
        sockets.close(self.socket)

    def send(self, msg):
        return sockets.send(self.socket,msg)

    def recv(self):
        return sockets.receive(self.socket)