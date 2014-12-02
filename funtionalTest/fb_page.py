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


#test lib
from TestLib import *


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







class TestMainPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)

    def testLoginLogout(self):
        self.driver.get(LOGIN_URL)
        self.driver.get(LOGOUT_URL)

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


class TestPostQuestion(HandlingQuestion):
    POST_BUTTON_ID = "fb_post_button"
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)
        self.question_info = 'this is a question'
        self.edit_question_info = 'this is a edited question'
        self.question_info_detail = ' this is a detail of question'
        self.edited_question_info_detail = ' this is a detail of question'

    def testPostEditDelete(self):
        """
         write more in one testcase to reduce the login activity
        """
        driver = self.driver
        self.post()
        #confirm the posted question
        question_info_result = driver.find_element_by_class_name('article_header')
        self.assertIn(question_info_result.text, self.question_info)
        self.edit_post()
        question_info_result = driver.find_element_by_class_name('article_header')
        self.assertIn(question_info_result.text, self.edit_question_info)
        self.delete_post()
        #check the url
        url_info = driver.current_url
        self.assertIn( os.path.join(BASE_URL , 'question_list'),url_info)
        #go to profile



    def tearDown(self):
        self.driver.close()

class TestShareTag(unittest.TestCase):
    def setUp(self):

        import os, subprocess
        os.chdir('/Users/mac/Documents/ChuotNhatTest/FunctionTest')
        subprocess.Popen(['python','clear_database.py'])


        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(FB_PAGE)
        self.Tag_handler = TagUtility(self.driver)

    def check_tag_suggesstion(self, Tag_handler,  tag_search_letter, existed_tag_list):
        tag_suggestion_list = Tag_handler.get_tag_suggestion(tag_search_letter)
        self.assertEqual(len(tag_suggestion_list),len(existed_tag_list))
        self.assertItemsEqual( existed_tag_list, tag_suggestion_list)

    def check_added_tag(self , tag_list):
        tag_added_list = self.Tag_handler.get_added_tag()
        self.assertItemsEqual(tag_added_list, tag_list )

    def testNewTag(self):

        Tag_handler = self.Tag_handler
        tag_list = ['Tag1','Tag2']
        tag_search_letter = 't'
        Tag_handler.add_new_tags(tag_list)
        self.check_added_tag( tag_list)
        save_button = self.driver.find_element_by_id('save_tag_list_button')
        save_button.click()
        self.driver.get(FB_PAGE)
        self.check_added_tag( tag_list)

        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)
        self.driver.refresh()
        self.check_added_tag(tag_list)

    def testUserAddManyTag(self):

        Tag_handler = self.Tag_handler
        tag_list = ['Tag1','Tag2','Tag3','Tag4','Tag5','Tag6']
        tag_search_letter = 't'
        Tag_handler.add_new_tags(tag_list)
        self.check_added_tag( tag_list)
        self.driver.get(FB_PAGE)
        self.check_added_tag( tag_list)
        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)

        new_tag_list = ['Tag1','Tag2']
        Tag_handler.add_new_tags(new_tag_list)
        self.check_added_tag( tag_list)
        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)

        #delte all tags
        Tag_handler.delete_all_user_tag_info()

        self.check_added_tag( [])
        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)
        self.driver.refresh()
        import pdb; pdb.set_trace()
        self.check_added_tag( [])
        self.check_tag_suggesstion(Tag_handler, tag_search_letter, tag_list)

    def testUncapitalTag(self):
        tag_list = ['Tag1','Tag2','Tag3','Tag4','Tag5','Tag6']
        self.Tag_handler.add_new_tags(tag_list)
        new_tag = 'tag1'
        tag_search_letter = 't'
        self.Tag_handler.add_new_tag(new_tag)
        self.check_added_tag( tag_list)
        self.check_tag_suggesstion(self.Tag_handler, tag_search_letter, tag_list)




    def testNewOneTag(self):
        new_tag = 'Tag3'
        self.Tag_handler.add_new_tag(new_tag)

        self.check_tag_suggesstion(self.Tag_handler, new_tag, [new_tag])
        self.check_added_tag( [new_tag])

    def tearDown(self):
        self.driver.close()



BASE_URL = option_handler(sys)


suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestMainPage))
suite.addTest(unittest.makeSuite(TestPostQuestion))
#suite.addTest(unittest.makeSuite(TestShareTag))
#suite.addTest(TestShareTag('testUserAddManyTag'))
unittest.TextTestRunner(verbosity=2).run(suite)
