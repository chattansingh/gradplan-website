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

    def test_profile(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:3000/choosemajor/')
        major= selenium.find_element_by_id('id_choose_major')
        submit = selenium.find_element_by_id('select')

        major.send_keys('Computer Engineering, B.S.')
        submit.send_keys(Keys.RETURN)