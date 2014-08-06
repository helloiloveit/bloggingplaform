__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testUnloginUser.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
import os, sys

LOCAL_TEST = "http://localhost:8002"
REAL_TEST ="http://www.chuotnhat.vn"
BASE_URL = REAL_TEST
#test user
EMAIL_TEST_USER_1='hrgohvb_bushakstein_1406709821@tfbnw.net'
PASS_TEST_USER_1='maiphuong'
EMAIL_TEST_USER_2='huhyrrm_liangsen_1407224530@tfbnw.net'
PASS_TEST_USER_2='maiphuong'
EMAIL_TEST_USER_3='heyrhvl_chaison_1407224525@tfbnw.net'
PASS_TEST_USER_3='maiphuong'
EMAIL_TEST_USER_4='vgeiufv_valtchanovsen_1407224521@tfbnw.net'
PASS_TEST_USER_4='maiphuong'
EMAIL_TEST_USER_5='qvimdwj_laverdetescu_1407224516@tfbnw.net'
PASS_TEST_USER_5='maiphuong'

def user_login(driver, test_user_email, test_user_pass):
    driver.get(LOGIN_URL)
    email = driver.find_elements_by_id('email')
    email[0].send_keys(test_user_email)
    pass_word = driver.find_elements_by_id('pass')
    pass_word[0].send_keys(test_user_pass)
    button_login = driver.find_elements_by_id('u_0_1')
    button_login[0].click()

def user_logout(driver):
    driver.get(LOGOUT_URL)

def multiple_user_login(driver1,driver2, driver3, driver4, driver5):
    user_login(driver1, EMAIL_TEST_USER_1, PASS_TEST_USER_1)
    user_login(driver2, EMAIL_TEST_USER_2, PASS_TEST_USER_2)
    user_login(driver3, EMAIL_TEST_USER_3, PASS_TEST_USER_3)
    user_login(driver4, EMAIL_TEST_USER_4, PASS_TEST_USER_4)
    user_login(driver5, EMAIL_TEST_USER_5, PASS_TEST_USER_5)


def like_a_question(like_button, count_like):
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
        return count_like
    return None

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



class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver1 = webdriver.Chrome()
        self.driver2 = webdriver.Chrome()
        self.driver3 = webdriver.Chrome()
        self.driver4 = webdriver.Chrome()
        self.driver5 = webdriver.Chrome()

    def userLogout(self):
        user_logout(self.driver1)
        user_logout(self.driver2)
        user_logout(self.driver3)
        user_logout(self.driver4)
        user_logout(self.driver5)

    def testUserInOut(self):
        multiple_user_login(self.driver1, self.driver2, self.driver3, self.driver4, self.driver5)
        self.userLogout()


    def tearDown(self):
        self.driver1.close()
        self.driver2.close()
        self.driver3.close()
        self.driver4.close()
        self.driver5.close()

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.driver1 = webdriver.Chrome()
        self.driver2 = webdriver.Chrome()
        self.driver3 = webdriver.Chrome()
        self.driver4 = webdriver.Chrome()
        self.driver5 = webdriver.Chrome()
        multiple_user_login(self.driver1, self.driver2, self.driver3, self.driver4, self.driver5)

    def followUser(self, driver):
        driver.get(QUESTION_LIST_URL)
        question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        first_question = question_list[0].find_element_by_class_name('article_popularity_info')
        profile_button = first_question.find_element_by_id('user_profile')
        profile_button.click()

    def testFollowFeature(self):
        import pdb; pdb.set_trace()
        self.followUser(self.driver1)
        self.followUser(self.driver2)
        self.followUser(self.driver3)
        self.followUser(self.driver4)
        self.followUser(self.driver5)



    def tearDown(self):
        self.driver1.close()
        self.driver2.close()
        self.driver3.close()
        self.driver4.close()
        self.driver5.close()



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
        popularity_info = self.driver.find_element_by_class_name('article_popularity_info')
        answer_button = popularity_info.find_element_by_id('inputCommentButton')
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
        user_info = answer_info.find_element_by_class_name('user_detail_info')
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




class TestHandlingQuestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.question_info = 'this is a question'
        self.edit_question_info = 'this is a edited question'
        self.question_info_detail = ' this is a detail of question'
        self.edited_question_info_detail = ' this is a detail of question'


    def post(self):
        driver = self.driver
        try:
            post_button = driver.find_element_by_id("post_button")
            post_button.click()
        except:

            sleep(2)
            post_button = driver.find_element_by_id("post_button")
            post_button.click()

        #add tag
        sleep(2)
        tag_info= driver.find_element_by_id('month')
        tag_info.click()
        tag_info.send_keys('c')
        try:
            temp = driver.find_element_by_id('suggestion_box')
        except:
            #wait for ajax call to finish
            print 'cant receive suggestion box'
            sleep(6)
            temp = driver.find_element_by_id('suggestion_box')
        tag_suggess = temp.find_element_by_xpath('div')
        tag_suggess.click()
        #post_tag_button = driver.find_element_by_id('submit1')
        #post_tag_button.click()
        #add question title
        question_info = driver.find_element_by_id('question_header')
        question_info.clear()
        question_info.send_keys(self.question_info)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.question_info_detail))
        submit_button = driver.find_element_by_id('post_question_button')
        submit_button.click()

    def delete_post(self):
        #delete post
        driver = self.driver
        delete_button = driver.find_element_by_id('delete_button')
        delete_button.click()
        yes_selection = driver.find_element_by_id('yes_selection')
        yes_selection.click()

    def edit_post(self):
        driver = self.driver
        edit_button = driver.find_element_by_id('edit_button')
        edit_button.click()
        question_info = driver.find_element_by_id('question_header')
        question_info.clear()
        question_info.send_keys(self.edit_question_info)
        #wait a bit for javascript to load to use tinymce api
        sleep(5)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.edited_question_info_detail))
        submit_button = driver.find_element_by_id('post_question_button')
        submit_button.click()



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



if sys.argv[1] == 'local':
    BASE_URL = LOCAL_TEST
    print '...start testing in local machine'
else:
    BASE_URL = REAL_TEST
    print'...start testing in real version'
LOGIN_URL = os.path.join(BASE_URL, 'user/login?_next=/')
LOGOUT_URL = os.path.join(BASE_URL, 'user/logout?_next=/')
QUESTION_LIST_URL = os.path.join(BASE_URL, 'question_list')

suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestAuth))
#suite.addTest(unittest.makeSuite(TestHandlingQuestion))
#suite.addTest(unittest.makeSuite(TestHandlingAnswer))
#suite.addTest(unittest.makeSuite(TestQuestionList))
suite.addTest(unittest.makeSuite(TestUserProfile))
unittest.TextTestRunner(verbosity=2).run(suite)
