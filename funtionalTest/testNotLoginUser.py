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

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def user_login(self):
        self.driver.get(LOGIN_URL)
        email = self.driver.find_elements_by_id('email')
        temp[0].send_keys('mhuy82gnr@yahoo.com')

        pass_word = self.driver.tempfind_elements_by_id('pass')
        pass_word[0].send_keys('lockcapsscroll2304')
        button_login = self.driver.find_elements_by_id('u_0_1')
        button_login[0].click()
        button_check_point = self.driver.find_elements_by_id('checkpointSubmitButton')
        button_check_point[0].click()
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

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    """
    def testUnRegisterGuestCheckUserProfile(self):
        driver = self.driver
        driver.get(BASE_URL)
        import pdb;pdb.set_trace()
    """
    def registeredUser_visit_his_Profile(self):
        driver = self.driver
        #click profile image
        profile_button = driver.find_element_by_id('user_profile')
        profile_button.click()

    def testVisitUserProfile(self):
        #go back
        question_list_button = self.driver.find_element_by_id('logo_site')
        question_list_button.click()
        #click on popularity panel
        user_profile = self.driver.find_element_by_id('user_profile')
        user_profile.click()
        #back

    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testViewQuestionByTag(self):
        pass


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
        answer_area = self.driver.find_element_by_class_name('user_comment')
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
#suite.addTest(unittest.makeSuite(TestAuth))
#suite.addTest(unittest.makeSuite(TestUserProfile))
suite.addTest(unittest.makeSuite(TestQuestionPage))
unittest.TextTestRunner(verbosity=2).run(suite)
