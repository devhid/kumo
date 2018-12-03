# bruteforce imports
from bruteforce.bruteforce import bruteforce

# configs imports
from configs import configs

# crawler imports
from crawler.crawler import Crawler

# funcs imports
from funcs.tokenizer import tokenize_html

# network imports
from network.Socket import Socket
from network.HttpRequest import HttpRequest

# utils imports
from utils.login_utils import detect_login
from utils.link_utils import dom_family
from utils.constants import HTTP_UA_CHROME

# tests imports
from tests.test_transform import TransformTest
from tests.test_link_utils import LinkUtilsTest
from tests.test_login_utils import LoginUtilsTest

if __name__ == "__main__":
    # Change the value of test to change what is tested
    tests = ["brute_force", "configs", "crawler", "http_local", "http_requests",
            "test_dom_family", "test_link_utils", "test_login_utils", "test_transform"]
    test = "crawler"

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
        response = request.send_get_request(url,host,ua)
        if response is not None:
            body = response.body

            # Detect if there is a login form present, and get login fields
            login = detect_login(body,host+url)
            if login is not None:
                form_url, user_key, pass_key, action_val = login
                words = tokenize_html(response.response, False)
                if "yalofaputu@autowb.com" in words and "test" in words:
                    words = {"yalofaputu@autowb.com","test"}
                # if "admin@mizio.io" in words:
                #     words = {"admin@mizio.io","admin"}
                post_req = HttpRequest(host, port, "POST")
                success = bruteforce(post_req, form_url, host, port, ua, user_key, pass_key, action_val, words)
                
                print("Successful Logins:")
                for cred in success:
                    print(f'    user = {cred.user}, pass = {cred.password}')
    elif test == "test_dom_family":
        dom_family("a.com", "b.a.com")
        dom_family("x.com", "x.com/login")
    elif test == "crawler":
        url = "http://3.17.9.15.xip.io/"
        # url = "http://email.kumo.x10host.com"
        method = "dfs"
        agent = HTTP_UA_CHROME
        depth = 10
        pages = 30
        
        crawler = Crawler()
        crawler.crawl(url, method, agent, depth, pages)
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
        response = request.send_get_request(url, host, ua)
        if response is not None:
            print(response.response)

        print("---------------")

        # Test POST login success
        request = HttpRequest(host, port, "POST")
        url = "/login"
        data = {"email":"admin@mizio.io", "password":"admin"}
        content_type = "application/x-www-form-urlencoded"
        body = HttpRequest.generate_post_body(content_type,data)
        content_length = len(body)

        if body is not None:
            response = request.send_post_request(url, host, ua, content_type, content_length, body)
            if response is not None:
                print(response.response)

        print("---------------")

        # Test POST login fail
        request = HttpRequest(host, port, "POST")
        url = "/login"
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"bademail@email.com", "password":"wrongpass"}
        body = HttpRequest.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            response = request.send_post_request(url, host, ua, content_type, content_length, body)
            if response is not None:
                print(response.response)

        print("---------------")

        # Test POST funform fail
        url = "/login"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin@mizio.net", "password":"admin"}
        request = HttpRequest(host, port, "POST")
        body = HttpRequest.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            response = request.send_post_request(url, host, ua, content_type, content_length, body)
            if response is not None:
                print(response.response)

        print("---------------")

        # Test POST funform fail
        url = "/funform"
        receive = True
        content_type = "application/x-www-form-urlencoded"
        data = {"email":"admin", "password":"wrongpass", "btn":"login"}
        request = HttpRequest(host, port, "POST")
        body = HttpRequest.generate_post_body(content_type,data)
        content_length = len(body)
        if body is not None:
            response = request.send_post_request(url, host, ua, content_type, content_length, body)
            if response is not None:
                print(response.response)

    # http_requests
    elif test == "http_requests":
        host = "3.17.9.125.xip.io"
        port = 80
        url = "/"
        ua = "chrome"
        num_get_req = 1

        # Test GET requests
        request = HttpRequest(host,port,"GET")
        for i in range(num_get_req):
            print("request %d" % (i))
            response = request.send_get_request(url,host,ua)
            if response is not None:
                print(response.response)
                body = response.body
                print(body)
                tuple_ = response.status_code
                status_code = tuple_[0] if tuple_ is not None else None
                redirect_url = tuple_[1] if tuple_ is not None else None
                if status_code is not None:
                    print("status code %s" % (status_code))
                    if status_code[:1] == "3":
                        print("redirect url %s" % (redirect_url))

        # Separate the output.
        print("---------------")

        # Test POST requests
        # url = "/post"
        # receive = True
        # content_type = "application/x-www-form-urlencoded"
        # data = {"hi":"world"}
        # num_post_req = 1
        # request = HttpRequest(host,port,"POST")
        # body = HttpRequest.generate_post_body(content_type,data)
        # content_length = len(body)
        # for i in range(num_post_req):
        #     print(f'Request {i}')
        #     print('-------------')
        #     if body is not None:
        #         response = request.send_post_request(url, host, ua, content_type, content_length, body)
        #         if response is not None:
        #             print(response.response)
        #             tuple_ = response.status_code
        #             status_code = tuple_[0] if tuple_ is not None else None
        #             redirect_url = tuple_[1] if tuple_ is not None else None
        #             if status_code is not None:
        #                 print("status code %s" % (status_code))
        #                 if status_code[:1] == "3":
        #                     print("redirect url %s" % (redirect_url))
    
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
