# bruteforce imports
from bruteforce.bruteforce import bruteforce

# configs imports
from configs import configs

# funcs imports
from funcs.tokenizer import tokenize_html

# http_requests imports
from http_requests.Socket import Socket
from http_requests.HttpRequest import HttpRequest

# utils imports
from utils.login_utils import detect_login

# tests imports
from tests.test_transform import TransformTest
from tests.test_link_utils import LinkUtilsTest
from tests.test_login_utils import LoginUtilsTest

if __name__ == "__main__":
    # Change the value of test to change what is tested
    tests = ["brute_force", "configs", "http_local", "http_requests",
            "test_link_utils", "test_login_utils", "test_transform"]
    test = "brute_force"
    if test not in tests:
        print(f"Test {test} is invalid.")
        pass

    # brute_force 
    if test == "brute_force":
        # host = "localhost"
        # port = 5000
        # url = "/login"
        # ua = "googlebot"

        host = "forum.3.17.9.125.xip.io"
        port = 80
        url = "/login/"
        ua = "chrome"

        request = HttpRequest(host, port, "GET")
        request.connect()
        sent_get = request.send_get_request(url, host, ua)
        if sent_get:
            response = request.receive()
            body = HttpRequest.get_body(response)

            # Detect if login form is present and get the login fields
            login = detect_login(body,host+url)
            if login is not None:
                print(login)
                form_url, user_key, pass_key, action_val = login

                words = tokenize_html(response, False)
                if "yalofaputu@autowb.com" in words and "test" in words:
                    words = {"yalofaputu@autowb.com","test"}
                # if "admin@mizio.io" in words:
                #     words = {"admin@mizio.io","admin"}
                post_req = HttpRequest(host, port, "POST")
                success = bruteforce(post_req, form_url, host, port, ua, user_key, pass_key, action_val, words)
                
                print("Successful Logins:")
                for cred in success:
                    print(f'    user = {cred.user}, pass = {cred.password}')

        request.close()

    # configs
    elif test == "configs":
        config = configs.DEFAULT_CONFIGS
        for val in config:
            print("%s : %s" % (val,config[val]))

    # http_local
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

    # http_requests
    elif test == "http_requests":
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
        body = HttpRequest.generate_post_body(content_type,data)
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
    
    # test_link_utils
    elif test == "test_link_utils":
        test_link_utils = LinkUtilsTest()
        test_link_utils.test_one_layer()
        test_link_utils.test_multiple_layers()
        test_link_utils.test_link_layer()
        test_link_utils.test_link_retrieval()
        test_link_utils.test_link_retrieval_layers()
        test_link_utils.test_link_retrieval_relative()
        test_link_utils.test_domain_family()
        print("test_link_utils passed")

    # test_login_utils
    elif test == "test_login_utils":
        test_login_utils = LoginUtilsTest()
        test_login_utils.test_login_detection()
        print("test_login_utils passed")

    # test_transform
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()
        print("test_transform passed")
