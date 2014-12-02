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


#lib
from TestLib import *

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

def click_like_unlike_button2(like_button, count_like):
    color = like_button.value_of_css_property('color')
    if color =='rgba(128, 128, 128, 1)':
        #not like this button yet
        like_button.click()
        sleep(4)
        color = like_button.value_of_css_property('color')
        if color == 'rgba(207, 9, 9, 1)':
            return  count_like + 1
    elif color == 'rgba(207, 9, 9, 1)':
        # already liked
        like_button.click()
        sleep(4)
        color = like_button.value_of_css_property('color')
        if color == 'rgba(128, 128, 128, 1)':
            return  count_like -1
    return None


def click_like_unlike_button(like_button):
    color = like_button.value_of_css_property('color')
    if color =='rgba(128, 128, 128, 1)':
    #not like this button yet
        like_button.click()
        sleep(4)
        color = like_button.value_of_css_property('color')
        if color == 'rgba(207, 9, 9, 1)':
            return True
    elif color == 'rgba(207, 9, 9, 1)':
        # already liked
        like_button.click()
        sleep(4)
        color = like_button.value_of_css_property('color')
        if color == 'rgba(128, 128, 128, 1)':
            return True
    return False

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()


    def testUserLogin(self):
        user_login(self.driver)
        driver = self.driver
        #user_info = driver.find_element_by_class_name("dropdown")
        #self.assertIn("Nguyen", user_info.text)
    def testUserLogout(self):
        user_login(self.driver)
        user_logout(self.driver)

        """
        elem = driver.find_element(by='id', value="logo_site")
        self.assertIn("Chuot nhat", elem.text)
        elem.click()
        """

    def tearDown(self):
        self.driver.close()

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(QUESTION_LIST_URL)

    def testFollowFeature(self):
        question_list = self.driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        first_question = question_list[0].find_element_by_class_name('article_popularity_info')
        profile_button = first_question.find_element_by_id('user_profile')
        profile_button.click()


    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testViewQuestionByTag(self):
        pass


class TestQuestionList(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver = webdriver.Firefox()
        user_login(self.driver)
        self.driver.get(QUESTION_LIST_URL)

    def testLikeaQuestion(self):
        """
        view each question in question_list once by onec
        """
        def like_unlike_question(question_info):
            question_unit = question_info.find_element_by_class_name('article_popularity_info')
            like_button = question_unit.find_element_by_class_name('like_unlike_button')
            count_like_info = question_info.find_element_by_class_name('count_like')
            before_click_count = int(count_like_info.text)
            #check if its clicked or not using color
            count_like = click_like_unlike_button2(like_button, before_click_count)
            after_click_count = int(count_like_info.text)
            self.assertTrue(count_like != None)
            self.assertTrue(count_like == after_click_count )

        question_list = self.driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        for i in range(0, len(question_list),1):
            like_unlike_question(question_list[i])


    def tearDown(self):
        self.driver.close()


class TestHandlingAnswer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.answer_info = 'this is an answer'
        self.answer_edit_info = 'this is an edited answer'
        self.driver.get(QUESTION_LIST_URL)
        question_one = self.driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()

    def postAnswer(self):
        popularity_info = self.driver.find_element_by_class_name('user_answer_option')
        answer_button = popularity_info.find_element_by_id('reply_question_button')
        answer_button.click()
        self.driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.answer_info))
        submit_button = self.driver.find_element_by_id('post_answer_button')
        submit_button.click()

    def deleteAnswer(self, handling_info):
        delete_button = handling_info.find_element_by_id('delete_answer_button')
        delete_button.click()
        yes_selection = self.driver.find_element_by_id('yes_selection')
        yes_selection.click()
        pass
    def editAnswer(self, handling_info):
        edit_button = handling_info.find_element_by_id('edit_answer_button')
        edit_button.click()
        sleep(3)
        self.driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.answer_edit_info))
        submit_button= self.driver.find_element_by_id('post_answer_button')
        submit_button.click()
        pass

    def AnswerElement(self, answer_info):
        user_profile = answer_info.find_element_by_id('user_profile')
        user_info = answer_info.find_element_by_class_name('user_profile_text')
        answer_text = answer_info.find_element_by_class_name('comment_info')
        handling_info = answer_info.find_element_by_class_name('article_popularity_info')
        try:
            like_button = handling_info.find_element_by_class_name('like_unlike_button')
            count_like_info = handling_info.find_element_by_class_name('count_like')
        except:
            self.assertTrue(false)
        pass

    def check_authority(self, answer_info):
        try:
            edit_button = answer_info.find_element_by_id('edit_answer_button')
            return True
        except NoSuchElementException:
            return False


    def LikeUnLikeFunction(self, answer_info):
        handling_info = answer_info.find_element_by_class_name('article_popularity_info')
        like_button = handling_info.find_element_by_class_name('like_unlike_button')
        count_like_info = handling_info.find_element_by_class_name('count_like')
        before_click_count = int(count_like_info.text)
        count_number = click_like_unlike_button2(like_button, before_click_count)
        after_click_count = int(count_like_info.text)
        self.assertTrue(count_number!= None)
        self.assertTrue(after_click_count == count_number)


    def testHandlingAnswer(self):
        # check number of answer available
        # to do : user another test user to create answer then test with it.  onwer of answer and not owner of answer
        popularity_info = self.driver.find_element_by_class_name('article_popularity_info')
        info = popularity_info.text.split(' ')
        if info[0] == '0':
            #no answer
            self.postAnswer()

        answer_list = self.driver.find_elements_by_xpath('//table[@class="article_comment_container"]//tbody//tr[@class="answer_unit"]')
        for i in range(0, len(answer_list),1):
            self.AnswerElement(answer_list[i])
            self.LikeUnLikeFunction(answer_list[i])
            if self.check_authority(answer_list[i]):
                self.editAnswer(answer_list[i])
            answer_list = self.driver.find_elements_by_xpath('//table[@class="article_comment_container"]//tbody//tr[@class="answer_unit"]')

        #delete question in loop
        answer_list = self.driver.find_elements_by_xpath('//table[@class="article_comment_container"]//tbody//tr[@class="answer_unit"]')
        i =0
        while i < len(answer_list):
            if self.check_authority(answer_list[i]):
                self.deleteAnswer(answer_list[i])
            answer_list = self.driver.find_elements_by_xpath('//table[@class="article_comment_container"]//tbody//tr[@class="answer_unit"]')
            i = i+1
        pass



    def tearDown(self):
        self.driver.close()




class TestHandlingQuestion(HandlingQuestion):
    POST_BUTTON_ID = "post_button"
    def setUp(self):
        #self.driver = webdriver.Firefox()
        super(TestPostQuestionTagHandling, self).setUp()
        user_login(self.driver)



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



class TestPostQuestionTagHandling(HandlingQuestion):
    POST_BUTTON_ID = "post_button"

    def setUp(self):
        super(TestPostQuestionTagHandling, self).setUp()
        #self.driver = webdriver.Firefox()
        user_login(self.driver)

    def random_tag_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def testUserManageTag(self):
        driver = self.driver
        self.compose_post()
        #add tag
        sleep(2)
        def post_new_tag(driver):
            tag_info= driver.find_element_by_id('month')
            tag_info.click()
            random_string= self.random_tag_generator(6)
            tag_info.send_keys(random_string)
            sleep(1)
            #select option in tag suggestion box
            try:
                temp = driver.find_element_by_id('suggestion_box')
            except:
                #wait for ajax call to finish
                print 'cant receive suggestion box'
                sleep(6)
                temp = driver.find_element_by_id('suggestion_box')
            tag_suggess = temp.find_element_by_xpath('div')
            tag_suggess.click()
            sleep(2)
            return random_string
        def post_a_tag(driver, tag_name):
            tag_info= driver.find_element_by_id('month')
            tag_info.click()
            tag_info.send_keys(tag_name)
            sleep(1)

        post_new_tag(driver)
        delete_point = driver.find_element_by_id('delete_tag')
        delete_point.click()

        # User post same tag
        posted_tag = post_new_tag(driver)
        post_a_tag(driver, posted_tag)
        delete_point = driver.find_elements_by_id('delete_tag')
        try:
            delete_point.click()
        except:
            delete_point[0].click()


    def tearDown(self):
        self.driver.close()

BASE_URL = option_handler(sys)


suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestAuth))
#suite.addTest(unittest.makeSuite(TestHandlingQuestion))
#suite.addTest(unittest.makeSuite(TestHandlingAnswer))
#suite.addTest(unittest.makeSuite(TestQuestionList))
#suite.addTest(unittest.makeSuite(TestUserProfile))
suite.addTest(unittest.makeSuite(TestPostQuestionTagHandling))
unittest.TextTestRunner(verbosity=2).run(suite)
