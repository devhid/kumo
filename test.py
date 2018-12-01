from tests.test_transform import *
from configs import configs
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest

if __name__ == "__main__":
    # Change the value of test to change what is tested
    test = "http_local"
    if test == "http_requests":
        host = "www.google.com"
        port = 80
        url = "/"
        ua = "chrome"

        # Test GET requests
        socket = Socket(host,port)
        request = HttpRequest(socket,"GET")
        socket.connect()
        sent_get = request.send_get_request(url,host,ua)
        if sent_get:
            response = socket.recv()
            print(response)
            tuple_ = HttpRequest.get_status_code(response)
            status_code = tuple_[0] if tuple_ is not None else None
            redirect_url = tuple_[1] if tuple_ is not None else None
            if status_code is not None:
                print("status code %s" % (status_code))
                if status_code[:1] == "3":
                    print("redirect url %s" % (redirect_url))
        socket.close()

        # Separate the output.
        print("---------------")

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
                tuple_ = HttpRequest.get_status_code(response)
                status_code = tuple_[0] if tuple_ is not None else None
                redirect_url = tuple_[1] if tuple_ is not None else None
                if status_code is not None:
                    print("status code %s" % (status_code))
                    if status_code[:1] == "3":
                        print("redirect url %s" % (redirect_url))
            socket.close()
<<<<<<< HEAD
    
    elif test == "http_local":
        host = "localhost"
        port = 5000
        url = "/"
        ua = "chrome"

        # Test GET
        socket = Socket("localhost",5000)
        request = HttpRequest(socket, "GET")
        socket.connect()
        sent_get = request.send_get_request(url,host,ua)
        if sent_get:
            response = socket.recv()
            print(response)
        socket.close()

        # Test POST login success
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin@mizio.io", "password":"admin"}
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

        # Test POST login fail
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"bademail@email.com", "password":"wrongpass"}
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

        # Test POST funform fail
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin@mizio.net", "password":"admin"}
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

        # Test POST funform fail
        url = "/funform"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin", "password":"wrongpass"}
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

=======
    elif test == "configs":
        config = configs.config
        for val in config:
            print("%s : %s" % (val,config[val]))
>>>>>>> master
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()