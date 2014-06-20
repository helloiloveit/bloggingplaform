__author__ = 'huyheo'

#python web2py.py -S welcome -M -R applications/welcome/funtionalTest/testPostQuestion.py

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
LOGIN_URL = "http://localhost:8002/user/login?_next=/"
LOGOUT_URL = "http://localhost:8002/user/logout?_next=/"


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def user_login(self):
        self.driver.get(LOGIN_URL)

    def user_logout(self):
        self.driver.get(LOGOUT_URL)

    def testUserLogin(self):
        self.user_login()
        driver = self.driver
        import pdb;pdb.set_trace()
        user_info = driver.find_element_by_class_name("dropdown")
        self.assertIn("Nguyen", user_info.text)
    def testUserLogout(self):
        self.user_login()
        self.user_logout()
        user_info = self.driver.find_element_by_class_name("dropdown")
        self.assertIn("Login", user_info.text)

        """
        elem = driver.find_element(by='id', value="logo_site")
        self.assertIn("Chuot nhat", elem.text)
        elem.click()
        """

    def tearDown(self):
        self.driver.close()

class TestPostNewArticle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(LOGIN_URL)

    def testPostNewArticle(self):
        import pdb;pdb.set_trace()
        post_button = self.driver.find_element_by_id("post_button")
        post_button.click()
    def tearDown(self):
        self.driver.close()



suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestAuth))
suite.addTest(unittest.makeSuite(TestPostNewArticle))
unittest.TextTestRunner(verbosity=2).run(suite)
