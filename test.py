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
        host = "facebook.com"
        port = 80
        url = "/safetycheck/"
        ua = "googlebot"
        num_get_req = 10

        # Test GET requests
        request = HttpRequest(host,port,"GET")
        for i in range(num_get_req):
            print("request %d" % (i))
            request.connect()
            sent_get = request.send_get_request(url,host,ua)
            if sent_get:
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
    elif test == "brute_force":
        host = "localhost"
        port = 5000
        url = "/login"
        ua = "googlebot"

        request = HttpRequest(host, port, "GET")
        request.connect()
        sent_get = request.send_get_request(url, host, ua)
        if sent_get:
            response = request.receive()
            print(response)

            # Detect if login form is present and get the login fields
            login_detected, user_key, pass_key, login_key = fetch_login_fields(response, "")
            print(f'Resp=[{login_detected}, {user_key}, {pass_key}, {login_key}]')

            if login_detected:
                words = tokenize_html(response) # Get list of words
                print(words)
                request = HttpRequest(host, port, "POST")
                bruteforce(request, url, host, port, ua, user_key, pass_key, words)

            # Send info for bruteforce
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
