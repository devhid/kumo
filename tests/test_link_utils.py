import unittest
from utils.link_utils import *
from utils.namedtuples import Form

class LinkUtilsTest(unittest.TestCase):

    def test_one_layer(self):
        tokenize_one_layer = tokenize_html('0000<html><head><title>Title</title></head><body><p>TestP TestP</p><h1>TestH1 TestH1</h1><span>TestSpan TestSpan</span><svg></svg></body></html>')
        assert tokenize_one_layer == set(['TestP', 'TestP', 'TestH1', 'TestH1', 'TestSpan', 'TestSpan'])

    def test_multiple_layers(self):
        tokenize_multiple_layers = tokenize_html('<html><body><p>TestP <span>TestSpan1</span></p><h1>TestH1 <span>TestSpan2 <span>TestSpan3</span></span></h1></body></html>')
        assert tokenize_multiple_layers == set(['TestP', 'TestSpan1', 'TestH1', 'TestSpan2', 'TestSpan3'])

    def test_link_layer(self):
        tokenize_link = tokenize_html('<html><body><p>TestP</p><h1>TestH1</h1><a href=https://google.com>Link </a><span>TestSpan</span></body></html>')
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
        #form_info = detect_login("", "http://kumo.x10host.com/login/")
        #assert form_info == True

        with open('./tests/login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        #print(tokenize_html(login_html))
        form_info = detect_login(login_html, "http://kumo.x10host.com/login/")
        assert form_info == Form(url='/login/', username='log', passname='pwd')

        with open('./tests/register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        form_info = detect_login(register_html, "http://kumo.x10host.com/register/")
        assert form_info == None

        with open('./tests/bootstrap_login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        form_info = detect_login(login_html, "http://base_url.com")
        assert form_info == Form(url='', username='email', passname='password')

        with open('./tests/bootstrap_register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        form_info = detect_login(register_html, "http://kumo.x10host.com")
        assert form_info == None

        with open('./tests/bootstrap_fun_form.txt', 'r') as fun_file:
            fun_html = fun_file.read().replace('\n', '')
        form_info = detect_login(fun_html, "http://base_url.com")
        assert form_info == Form(url='', username='email', passname='password')

    def test_domain_family(self):
        assert dom_family('a.b.c.com', 'c.com') == True
        assert dom_family('a.b.c.com', 'b.c.com') == True
        assert dom_family('a.b.c.com', 'a.b.c.com') == True
        assert dom_family('b.com', 'a.b.com') == True
        assert dom_family('a.com', 'a.b.com') == False
        assert dom_family('a.b.c.d.e.com', 'a.b.c.e.com') == False
        
