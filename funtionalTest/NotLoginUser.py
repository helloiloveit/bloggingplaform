__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/AfterLogin.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
import os
import sys

LOCAL_TEST = "http://localhost:8002"
REAL_TEST ="http://chuotnhat.vn"
#BASE_URL = REAL_TEST
BASE_URL = LOCAL_TEST
LOGIN_URL = os.path.join(BASE_URL, 'user/login?_next=/')
LOGOUT_URL = os.path.join(BASE_URL, 'user/logout?_next=/')
QUESTION_LIST_URL = os.path.join(BASE_URL, 'question_list')

NUM_OF_QUESTION_PER_PAGE = 12

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def getToUserProfile(self, driver):
        driver.get(QUESTION_LIST_URL)
        question_one = driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()
        #click on writer of question
        user_profile = driver.find_element_by_id('user_profile')
        user_profile.click()
    def testVisitUserProfileInQuestion(self):
        self.getToUserProfile(self.driver)

    def testClickableFirstPage(self):
        self.getToUserProfile(self.driver)
        TestUserProfile.viewAllQuestionInList(self.driver)

    def testClickableSecondPage(self):
        question_list = self.driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
        number_of_question = len(question_list)
        if number_of_question < NUM_OF_QUESTION_PER_PAGE:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                self.assertTrue(False)
            except:
                self.assertTrue(True)
        else:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                view_more_button.click()
                TestUserProfile.viewAllQuestionInList(self.driver)
            except:
                self.assertTrue(False)

    @staticmethod
    def questionElement( question_info, driver):
        try:
            question_unit = question_info.find_element_by_class_name('article_header')
            answer_info = question_info.find_element_by_class_name('user_answer_info')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()
            return True
        except:
            return False


    @staticmethod
    def viewAllQuestionInList( driver):
        question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
        number_of_question = len(question_list)
        for i in range(0, number_of_question,1):
            sleep(4)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
            rst =TestUserProfile.questionElement(question_list[i], driver)
            return rst
        return False



    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(QUESTION_LIST_URL)

    def questionElement(self, question_info, driver):
        try:
            tag_info = question_info.find_element_by_class_name('article_tag')
            question_unit = question_info.find_element_by_class_name('article_header')
            question_detail_info = question_info.find_element_by_class_name('article_introduction')
            popularity_info = question_info.find_element_by_class_name('article_popularity_info')
            register_to_like = popularity_info.find_element_by_class_name('register_to_like')
            count_like= popularity_info.find_element_by_class_name('count_like')
            answer_info= popularity_info.find_element_by_class_name('popularity_a_tag_text')
            user_profile= popularity_info.find_element_by_id('user_profile')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()
            return True
        except:
            return False

    def viewAllQuestionInList(self, driver):
        """
        view each question in question_list once by onec
        """
        question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        number_of_question = len(question_list)
        for i in range(0, number_of_question,1):
            sleep(6)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
            print len(question_list)
            rst = self.questionElement(question_list[i], driver)
            self.assertTrue(rst)

        pass
    def testClickableFirstPage(self):
        self.viewAllQuestionInList(self.driver)

    def testClickableSecondPage(self):
        question_list = self.driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        number_of_question = len(question_list)
        if number_of_question < NUM_OF_QUESTION_PER_PAGE:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                self.assertTrue(False)
            except:
                self.assertTrue(True)
        else:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                view_more_button.click()
                self.viewAllQuestionInList(self.driver)
            except:
                self.assertTrue(False)


    def tearDown(self):
        self.driver.close()


class TestQuestionPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)
        self.answer_button_text = 'tra loi'
        self.answer_text   = 'quan diem'
        self.driver.get(QUESTION_LIST_URL)
        question_one = self.driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()


    def questionElement(self):
        #check if no answer button is there
        try:
            tag_info = self.driver.find_element_by_class_name('article_tag')
            question_info=self.driver.find_element_by_class_name('article_header')
            question_detail_info=self.driver.find_element_by_class_name('article_introduction')
            popularity_info=self.driver.find_element_by_class_name('article_popularity_info')
            user_profile = popularity_info.find_element_by_id('user_profile')

        except:
            return False
        try:
            self.driver.find_element_by_id('inputCommentButton')
            return False
        except NoSuchElementException:
            pass

        return True
        #click on  question on right side bar
        """
        side_bar_questions = self.driver.find_element_by_id('right_bar_question_list')
        question = side_bar_questions.find_element_by_id('related_question')
        question.click()
        self.driver.back()
        """
    def answerElement(self, answer_info):
        """
        check element of answer
        """
        try:
            user_info = self.driver.find_element_by_class_name('user_info')
            user_profile = user_info.find_element_by_id('user_profile')
            user_detail_info = user_info.find_element_by_class_name('user_detail_info')
            comment_info = answer_info.find_element_by_class_name('comment_info')
            popularity_info = answer_info.find_element_by_class_name('article_popularity_info')
            count_like_info = popularity_info.find_element_by_class_name('count_like')
            register_to_like = popularity_info.find_element_by_class_name('register_to_like')
        except:
            return False
        return True


    def testAnswer(self):
        #in first question
        answer_area = self.driver.find_element_by_class_name('article_popularity_info')
        info = answer_area.text.split(' ')
        if info[0] == '0':
            #no answer
            pass
        else:
            answer_list = self.driver.find_elements_by_xpath('//table[@class="article_comment_container"]//tbody//tr[@class="answer_unit"]')
            number_of_answer = len(answer_list)
            for i in range(0, number_of_answer, 1):
                sleep(3)
                rst = self.answerElement(answer_list[i])
                self.assertTrue(rst)
            pass

    def testQuestion(self):
        rst = self.questionElement()
        self.assertTrue(rst)






    """
    def testPopularityInfoOfQuestionInQuestionList(self):
        popularity_info = self.driver.find_element_by_class_name('article_popularity_info')
        answer_button = popularity_info.find_elements_by_xpath("//*[contains(text(), 'tra loi')]")
        answer_button[0].click()
        self.driver.back()
        pass
    """



    def tearDown(self):
        self.driver.close()

class TestAnswer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        pass
    def tearDown(self):
        self.driver.close()

if sys.argv[1] == 'local':
    BASE_URL = LOCAL_TEST
    print '...start testing in local machine'
else:
    BASE_URL = REAL_TEST
    print'...start testing in real version'

suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestUserProfile))
suite.addTest(unittest.makeSuite(TestQuestionPage))
#suite.addTest(unittest.makeSuite(TestAnswer))
#suite.addTest(unittest.makeSuite(TestQuestionListPage))
#suite.addTest(unittest.makeSuite(TestUserProfile))
unittest.TextTestRunner(verbosity=2).run(suite)
