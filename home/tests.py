from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Safari()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/accounts/register/')
        username= selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password = selenium.find_element_by_id('id_password1')
        confirmed_password = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_id('register')

        username.send_keys('chattan12')
        email.send_keys('chattansingh.chattansingh.137@my.csun.edu')
        password.send_keys('Password123')
        confirmed_password.send_keys('Password123')
        submit.send_keys(Keys.RETURN)
        #assert  in selenium.page_source




