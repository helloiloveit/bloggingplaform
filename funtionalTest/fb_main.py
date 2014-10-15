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

    def add_new_tag(self, tag_name):
        tag_info= self.driver.find_element_by_id('typing_box')
        tag_info.click()
        tag_info.send_keys(tag_name)
        sleep(2)
        temp = self.driver.find_element_by_id('suggestion_box')
        temp.click()

    def add_new_tags(self, tag_list):
        for tag_info in tag_list:
            self.add_new_tag(tag_info)

    def get_tag_suggestion(self, input_tag):
        tag_info= self.driver.find_element_by_id('typing_box')
        tag_info.click()
        sleep(1)
        tag_info.send_keys(input_tag)
        sleep(2)
        temp = self.driver.find_element_by_id('suggestion_box')
        tag_suggess = temp.find_elements_by_xpath('div')
        tag_suggess_list = []
        for data in tag_suggess:
            tag_suggess_list.append(data.text)
        return tag_suggess_list




class TestMainPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)


    def testDisplay(self):
        question_button = self.driver.find_element_by_id('fb_post_button')
        question_button.click()
        self.driver.back()
        sleep(2)
        tag_info= self.driver.find_element_by_id('typing_box')
        tag_info.click()

        #share_tag_button = self.driver.find_element_by_id('share_knownledge_header')
        pass

    def tearDown(self):
        self.driver.close()

class TestShareTag(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)

    def check_tag_suggesstion(self, Tag_handler,  tag_search_letter, existed_tag_list):
        tag_suggestion_list = Tag_handler.get_tag_suggestion(tag_search_letter)
        self.assertEqual(len(tag_suggestion_list),len(existed_tag_list))
        self.assertEqual( existed_tag_list, tag_suggestion_list)


    def testNewTag(self):

        Tag_handler = TagUtility(self.driver)
        tag_list = ['Tag1','Tag2']
        tag_search_letter = 't'
        Tag_handler.add_new_tags(tag_list)

        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)

        new_tag = 'Tag3'
        Tag_handler.add_new_tag(new_tag)

        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list.append(new_tag))


    def tearDown(self):
        self.driver.close()



BASE_URL = option_handler(sys)


suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestMainPage))
suite.addTest(unittest.makeSuite(TestShareTag))
unittest.TextTestRunner(verbosity=2).run(suite)
