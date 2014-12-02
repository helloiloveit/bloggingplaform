__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/TestBasicFunction.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
import os
import sys
from option_handler import *
from PageElementInfoLib import *



class TestUserProfile(unittest.TestCase, ProfilePage):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def getToUserProfile(self, driver):
        driver.get(QUESTION_LIST_URL)
        try:
            question_one = driver.find_element_by_class_name('article_header')
            link = question_one.find_element_by_link_text(question_one.text)
            link.click()
            #click on writer of question
            user_profile = driver.find_element_by_id('user_profile')
            user_profile.click()
        except:
            print'Error: check question list '
            return False

    def testClickableFirstPage(self):
        self.getToUserProfile(self.driver)
        self.viewAllQuestionInList(self.driver)

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
                self.viewAllQuestionInList(self.driver)
            except:
                self.assertTrue(False)


    def viewAllQuestionInList(self, driver):
        question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
        for i in range(0, len(question_list),1):
            sleep(4)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="user_activity_info"]//tbody//tr[@class="question_unit"]')
            rst =self.questionElement(question_list[i], driver)
            return rst
        return False



    def tearDown(self):
        self.driver.close()


class TestQuestionListPage(unittest.TestCase, QuestionList):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(QUESTION_LIST_URL)


    def viewAllQuestionInList(self, driver):
        """
        view each question in question_list once by onec
        """
        question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        number_of_question = len(question_list)
        for i in range(0, number_of_question ,1):
            sleep(6)
            print'click on question number %d' %i
            question_list = driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
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


class TestQuestionPage(unittest.TestCase, QuestionPage):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)
        self.driver.get(QUESTION_LIST_URL)
        question_one = self.driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()

    def answer_of_question(self):
        #in first question
        #go thought each answer of first question
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
                print'checking answer number: ',i
                rst = self.answerElement(answer_list[i])

                self.assertTrue(rst)
            pass

    def testDisplayElementInQuestionPage(self):
        rst = self.questionElement()
        self.assertTrue(rst)
        self.answer_of_question()



    def tearDown(self):
        self.driver.close()



BASE_URL =  option_handler(sys)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUserProfile))
#suite.addTest(unittest.makeSuite(TestQuestionPage))
#suite.addTest(unittest.makeSuite(TestQuestionListPage))
unittest.TextTestRunner(verbosity=2).run(suite)
