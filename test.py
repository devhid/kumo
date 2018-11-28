from tests.test_transform import *
import http_requests.sockets as sockets

if __name__ == "__main__":
    # Change the value of test to change what is tested
    test = "http_requests"
    if test == "http_requests":
        host = "google.com"
        port = 80
        url = "/"
        ua = "chrome"

        socket = sockets.connect(host,port)
        sent_get = sockets.send_get_request(socket,url,host,ua)
        if sent_get:
            response = sockets.receive(socket)
            print("response %s" % (response))
            
        sockets.close(socket)
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()