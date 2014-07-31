__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testAfterLogin.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
BASE_URL = "http://localhost:8002/"
LOGIN_URL = "http://localhost:8002/user/login?_next=/"
LOGOUT_URL = "http://localhost:8002/user/logout?_next=/"
QUESTION_LIST_URL = "http://localhost:8002/chuotnhat/default/question_list"

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
                self.assertTrue(false)
            except:
                self.assertTrue(True)
        else:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                view_more_button.click()
                TestUserProfile.viewAllQuestionInList(self.driver)
            except:
                self.assertTrue(false)



    @staticmethod
    def viewAllQuestionInList( driver):
        question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
        number_of_question = len(question_list)
        for i in range(0, number_of_question,1):
            sleep(6)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
            question_unit = question_list[i].find_element_by_class_name('article_header')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()


    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(QUESTION_LIST_URL)

    def viewAllQuestionInList(self, driver):
        """
        view each question in question_list once by onec
        """
        question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        number_of_question = len(question_list)
        import pdb;pdb.set_trace()
        for i in range(0, number_of_question,1):
            sleep(6)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
            print len(question_list)
            question_unit = question_list[i].find_element_by_class_name('article_header')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()

        pass
    def testClickableFirstPage(self):
        self.viewAllQuestionInList(self.driver)

    def testClickableSecondPage(self):
        question_list = self.driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        number_of_question = len(question_list)
        if number_of_question < NUM_OF_QUESTION_PER_PAGE:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                self.assertTrue(false)
            except:
                self.assertTrue(True)
        else:
            try:
                view_more_button = self.driver.find_element_by_id('view_more_question')
                view_more_button.click()
                self.viewAllQuestionInList(self.driver)
            except:
                self.assertTrue(false)


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

    def testInfoOfQuestion(self):
        #check if no answer button is there
        try:
            self.driver.find_element_by_id('inputCommentButton')
        except NoSuchElementException:
            pass
        #click on writer of question
        user_profile = self.driver.find_element_by_id('user_profile')
        user_profile.click()
        self.driver.back()

        #click on  question on right side bar
        """
        side_bar_questions = self.driver.find_element_by_id('right_bar_question_list')
        question = side_bar_questions.find_element_by_id('related_question')
        question.click()
        self.driver.back()
        """

    def testInfoOfAnswer(self):
        #in first question
        answer_area = self.driver.find_element_by_class_name('article_popularity_info')
        info = answer_area.text.split(' ')
        if info[0] == '0':
            #no answer
            pass
        else:
            answer_area = self.driver.find_element_by_class_name("article_comment_container")
            user_profile = answer_area.find_element_by_id('user_profile')
            user_profile.click()
            self.driver.back()
            pass





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

suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestUserProfile))
#suite.addTest(unittest.makeSuite(TestQuestionPage))
#suite.addTest(unittest.makeSuite(TestQuestionListPage))
suite.addTest(unittest.makeSuite(TestUserProfile))
unittest.TextTestRunner(verbosity=2).run(suite)
