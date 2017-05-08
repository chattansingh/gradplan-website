from django.test import TestCase, LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ProfileTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Safari()
        super(ProfileTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ProfileTestCase, self).tearDown()

    def test_login(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:3000/login/')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')

        username.send_keys('chattan12')
        password.send_keys('Password123')
        submit.send_keys(Keys.RETURN)
       # assert 'Successfully saved' in selenium.page_source

    def test_profile(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:3000/profile/')
        major = selenium.find_element_by_id('id_current_major')
        submit = selenium.find_element_by_id('save')

        major.send_keys('Computer Science, B.S.')
        submit.send_keys(Keys.RETURN)