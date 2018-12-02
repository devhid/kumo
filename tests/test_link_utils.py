import unittest
from utils.link_utils import *

class LinkUtilsTest(unittest.TestCase):

    def test_one_layer(self):
        tokenize_one_layer = tokenize_html('<html><p>TestP TestP</p><h1>TestH1 TestH1</h1><span>TestSpan TestSpan</span></html>')
        assert tokenize_one_layer == set(['TestP', 'TestP', 'TestH1', 'TestH1', 'TestSpan', 'TestSpan'])

    def test_multiple_layers(self):
        tokenize_multiple_layers = tokenize_html('<html><p>TestP <span>TestSpan1</span></p><h1>TestH1 <span>TestSpan2 <span>TestSpan3</span></span></h1></html>')
        assert tokenize_multiple_layers == set(['TestP', 'TestSpan1', 'TestH1', 'TestSpan2', 'TestSpan3'])

    def test_link_layer(self):
        tokenize_link = tokenize_html('<html><p>TestP</p><h1>TestH1</h1><a href=https://google.com>Link </a><span>TestSpan</span></html>')
        assert tokenize_link == set(['TestP', 'TestH1', 'Link', 'TestSpan'])

    def test_link_retrieval(self):
        links = retrieve_links("<html><a href=https://google.com>Link</a><a href=https://amazon.com>TestSpan</a><a href=https://google.com#fragment>Link</a><a href=https://amazon.com/#fragment>TestSpan</a></html>", "")
        assert links == set(['https://google.com', 'https://amazon.com'])

    def test_link_retrieval_layers(self):
        links = retrieve_links("<html><p>TestP</p><h1>TestH1</h1><a href=https://google.com>Link </a><span><a href=https://amazon.com>TestSpan</a></span></html>", "")
        assert links == set(['https://google.com', 'https://amazon.com'])

    def test_link_retrieval_relative(self):
        links = retrieve_links("<html><a href=\"\">Link</a><a href=./>Link</a><a href=/>Link</a><a href=./>Link</a><a href=../>Link</a><a href=./kumo>Link</a><a href=../devhid>TestSpan</a></html>", "https://github.com/devhid/")
        assert links == set(['https://github.com', 'https://github.com/devhid', 'https://github.com/devhid/kumo'])

    def test_login_detection(self):
        #login_detected = detect_login("", "http://kumo.x10host.com/login/")
        #assert login_detected == True

        with open('./tests/login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        login_detected = detect_login(login_html, "http://kumo.x10host.com")
        assert login_detected == ["http://kumo.x10host.com/login/", "user_login", "user_pass"]

        with open('./tests/register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        login_detected = detect_login(register_html, "http://kumo.x10host.com")
        assert login_detected == None

        with open('./tests/bootstrap_login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        login_detected = detect_login(login_html, "http://base_url.com")
        assert login_detected == ["http://base_url.com", "email", "password"]

        with open('./tests/bootstrap_register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        login_detected = detect_login(register_html, "http://kumo.x10host.com")
        assert login_detected == None

        with open('./tests/bootstrap_fun_form.txt', 'r') as fun_file:
            fun_html = fun_file.read().replace('\n', '')
        login_detected = detect_login(fun_html, "http://base_url.com")
        assert login_detected == ["http://base_url.com", "email", "password"]