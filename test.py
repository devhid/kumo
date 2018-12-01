from tests.test_transform import *
from configs import configs
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest

if __name__ == "__main__":
    # Change the value of test to change what is tested
    test = "http_requests"
    if test == "http_requests":
        host = "httpbin.org"
        port = 80
        url = "/get"
        ua = "chrome"

        # Test GET requests
        socket = Socket(host,port)
        request = HttpRequest(socket,"GET")
        socket.connect()
        sent_get = request.send_get_request(url,host,ua)
        if sent_get:
            response = socket.recv()
            print(response)
        socket.close()

        # Test POST requests
        url = "/post"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"hi":"world"}
        request = HttpRequest(socket,"POST")
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            socket.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = socket.recv()
                print(response)
            socket.close()
    elif test == "configs":
        config = configs.config
        for val in config:
            print("%s : %s" % (val,config[val]))
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()