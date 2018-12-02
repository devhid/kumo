from tests.test_transform import *
from tests.test_link_utils import *
from configs import configs
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest
from utils.link_utils import *
from bruteforce.bruteforce import *

if __name__ == "__main__":
    # Change the value of test to change what is tested
    test = "brute_force"
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
        num_post_req = 10
        request = HttpRequest(host,port,"POST")
        body = request.generate_post_body(content_type,data)
        content_length = len(body)
        for i in range(num_post_req):
            print(f'request {i}')
            print('-------------')
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

    elif test == "brute_force":
        # host = "localhost"
        # port = 5000
        # url = "/login"
        # ua = "googlebot"

        host = "email.kumo.x10host.com"
        port = 80
        url = "/login/"
        ua = "chrome"

        request = HttpRequest(host, port, "GET")
        request.connect()
        sent_get = request.send_get_request(url, host, ua)
        if sent_get:
            response = request.receive()
            body = request.get_body(response)
            # print(body)

            # Detect if login form is present and get the login fields
            login = detect_login(body,host+url)
            if login is not None:
                form_url, user_key, pass_key = login

                words = tokenize_html(body)
                # if "bawofafefe@kulmeo.com" in words and "Test12345!" in words:
                #     words = {"bawofafefe@kulmeo.com","Test12345!"}
                # print(words)
                post_req = HttpRequest(host, port, "POST")
                success = bruteforce(post_req, form_url, host, port, ua, user_key, pass_key, words)
                
                print("Successful Logins:")
                for cred in success:
                    print(f'    user = {cred.user}, pass = {cred.password}')

        request.close()

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
    elif test == "test_link_utils":
        test_link_utils = LinkUtilsTest()
        test_link_utils.test_one_layer()
        test_link_utils.test_multiple_layers()
        test_link_utils.test_link_layer()
        test_link_utils.test_link_retrieval()
        test_link_utils.test_link_retrieval_layers()
        test_link_utils.test_link_retrieval_relative()
        test_link_utils.test_login_detection()
        test_link_utils.test_domain_family()
        print("Test passed")
