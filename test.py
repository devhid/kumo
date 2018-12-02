from tests.test_transform import *
from tests.test_link_utils import *
from configs import configs
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest


if __name__ == "__main__":
    # Change the value of test to change what is tested
<<<<<<< HEAD
    test = "http_local"
=======
    test = "test_link_utils"
>>>>>>> feature/list_utils
    if test == "http_requests":
        host = "httpbin.org"
        port = 80
        url = "/get"
        ua = "chrome"
        num_get_req = 1

        # Test GET requests
        request = HttpRequest(host,port,"GET")
        for i in range(num_get_req):
            print("request %d" % (i))
            request.connect()
            sent_get = request.send_get_request(url,host,ua)
            if sent_get:
                response = request.receive()
                print(response)
                body = request.get_body(response)
                print(body)
                tuple_ = HttpRequest.get_status_code(response)
                status_code = tuple_[0] if tuple_ is not None else None
                redirect_url = tuple_[1] if tuple_ is not None else None
                if status_code is not None:
                    print("status code %s" % (status_code))
                    if status_code[:1] == "3":
                        print("redirect url %s" % (redirect_url))
            request.close()

        # Separate the output.
        print("---------------")

        # Test POST requests
        url = "/post"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"hi":"world"}
        request = HttpRequest(host,port,"POST")
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            request.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = request.receive()
                print(response)
                tuple_ = HttpRequest.get_status_code(response)
                status_code = tuple_[0] if tuple_ is not None else None
                redirect_url = tuple_[1] if tuple_ is not None else None
                if status_code is not None:
                    print("status code %s" % (status_code))
                    if status_code[:1] == "3":
                        print("redirect url %s" % (redirect_url))
            request.close()
    
    elif test == "http_local":
        host = "localhost"
        port = 5000
        url = "/"
        ua = "chrome"

        # Test GET
        request = HttpRequest(host, port, "GET")
        request.connect()
        sent_get = request.send_get_request(url, host, ua)
        if sent_get:
            response = request.receive()
            print(response)
        request.close()

        print("---------------")

        # Test POST login success
        request = HttpRequest(host, port, "POST")
        url = "/login"
        receive = True
        data = {"email":"admin@mizio.io", "password":"admin"}
        content_type = "application/x-www-form-urlencoded"
        body = request.generate_post_body(content_type,data)
        content_length = len(body)

        if body is not None:
            request.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = request.receive()
                print(response)
            request.close()

        print("---------------")

        # Test POST login fail
        request = HttpRequest(host, port, "POST")
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"bademail@email.com", "password":"wrongpass"}
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            request.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = request.receive()
                print(response)
            request.close()

        print("---------------")

        # Test POST funform fail
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin@mizio.net", "password":"admin"}
        request = HttpRequest(host, port, "POST")
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            request.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = request.receive()
                print(response)
            request.close()

        print("---------------")

        # Test POST funform fail
        url = "/funform"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin", "password":"wrongpass", "btn":"login"}
        request = HttpRequest(host, port, "POST")
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            request.connect()
            sent_get = request.send_post_request(url, host, ua, content_type, content_length, body)
            if sent_get and receive:
                response = request.receive()
                print(response)
            request.close()

    elif test == "configs":
        config = configs.config
        for val in config:
            print("%s : %s" % (val,config[val]))
            request.close()
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()
    elif test == "test_link_utils":
        test_link_utils = LinkUtilsTest()
        test_link_utils.test_one_layer()
        test_link_utils.test_multiple_layers()
        test_link_utils.test_link_layer()
        test_link_utils.test_link_retrieval()
        test_link_utils.test_link_retrieval_layers()
        test_link_utils.test_link_retrieval_relative()
        test_link_utils.test_login_detection()
