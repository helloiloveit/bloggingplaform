__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testUnloginUser.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
import os, sys
import string, random
from option_handler import *

FB_PAGE = 'http://localhost:8002/fb_main'

#test user
EMAIL_TEST_USER_1='hrgohvb_bushakstein_1406709821@tfbnw.net'
PASS_TEST_USER_1='maiphuong'
"""
def user_login_real_user(self):
    self.driver.get(LOGIN_URL)
    email = self.driver.find_elements_by_id('email')
    email[0].send_keys('mhuy82gnr@yahoo.com')
    pass_word = self.driver.find_elements_by_id('pass')
    pass_word[0].send_keys('lockcapsscroll2304')
    button_login = self.driver.find_elements_by_id('u_0_1')
    button_login[0].click()
    button_check_point = self.driver.find_elements_by_id('checkpointSubmitButton')
    button_check_point[0].click()
"""

def user_login(driver):
    driver.get(LOGIN_URL)
    email = driver.find_elements_by_id('email')
    email[0].send_keys(EMAIL_TEST_USER_1)
    pass_word = driver.find_elements_by_id('pass')
    pass_word[0].send_keys(PASS_TEST_USER_1)
    button_login = driver.find_elements_by_id('u_0_1')
    button_login[0].click()

def user_logout(driver):
    driver.get(LOGOUT_URL)


class TagUtility(object):
    """
    tool for handling user tag info
    """
    def __init__(self, driver):
        self.driver = driver

    def delete_user_tag_info(self):
        tag_list = self.driver.find_elements_by_class_name('post-tag')
        if len(tag_list):
            for tag_unit in tag_list:
                tag_del_but = tag_unit.find_element_by_id('delete_tag')
                tag_del_but.click()
            save_button = self.driver.find_element_by_id('save_tag_list_button')
            save_button.click()


class TestMainPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)

    def testDisplay(self):
        print 'llaa'
        question_button = self.driver.find_element_by_id('fb_post_button')
        question_button.click()
        self.driver.back()
        share_tag_button = self.driver.find_element_by_id('share_knownledge_header')

    def testShareTag(self):
        import pdb; pdb.set_trace()
        #check tag ..delete if there's any existing one.
        TagUtility(self.driver).delete_user_tag_info()

        #update new tag




    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testViewQuestionByTag(self):
        pass



BASE_URL = option_handler(sys)


suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestAuth))
#suite.addTest(unittest.makeSuite(TestHandlingQuestion))
#suite.addTest(unittest.makeSuite(TestHandlingAnswer))
#suite.addTest(unittest.makeSuite(TestQuestionList))
#suite.addTest(unittest.makeSuite(TestUserProfile))
suite.addTest(unittest.makeSuite(TestMainPage))
unittest.TextTestRunner(verbosity=2).run(suite)
