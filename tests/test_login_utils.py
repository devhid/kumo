# python imports
import unittest

# utils imports
from utils.login_utils import detect_login
from utils.namedtuples import Form

class LoginUtilsTest(unittest.TestCase):
    def test_login_detection(self):
        #form_info = detect_login("", "http://kumo.x10host.com/login/")
        #assert form_info == True

        with open('./tests/login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        #print(tokenize_html(login_html))
        form_info = detect_login(login_html, "http://kumo.x10host.com/login/")
        assert form_info == Form(url='/login/', username='log', passname='pwd', action='login')

        with open('./tests/register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        form_info = detect_login(register_html, "http://kumo.x10host.com/register/")
        assert form_info == None

        with open('./tests/bootstrap_login_test.txt', 'r') as login_file:
            login_html = login_file.read().replace('\n', '')
        form_info = detect_login(login_html, "http://base_url.com")
        assert form_info == Form(url='', username='email', passname='password', action='')

        with open('./tests/bootstrap_register_test.txt', 'r') as register_file:
            register_html = register_file.read().replace('\n', '')
        form_info = detect_login(register_html, "http://kumo.x10host.com")
        assert form_info == None

        with open('./tests/bootstrap_fun_form.txt', 'r') as fun_file:
            fun_html = fun_file.read().replace('\n', '')
        form_info = detect_login(fun_html, "http://base_url.com")
        assert form_info == Form(url='', username='email', passname='password', action='')