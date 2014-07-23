__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testPostQuestion.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
BASE_URL = "http://localhost:8002/"
LOGIN_URL = "http://localhost:8002/user/login?_next=/"
LOGOUT_URL = "http://localhost:8002/user/logout?_next=/"
QUESTION_LIST_URL = "http://localhost:8002/welcome/default/question_list"

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


    def tearDown(self):
        self.driver.close()

class TestQuestionListPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testViewQuestionByTag(self):
        pass

class TestPostNewArticle(unittest.TestCase):
    def setUp(self):
        import pdb;pdb.set_trace()
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.user_login()
        self.question_info = 'this is a question'
        self.edit_question_info = 'this is a edited question'
        self.question_info_detail = ' this is a detail of question'
        self.edited_question_info_detail = ' this is a detail of question'

    def user_login(self):
        self.driver.get(LOGIN_URL)
        email = self.driver.find_elements_by_id('email')
        email[0].send_keys('mhuy82gnr@yahoo.com')

        pass_word = self.driver.find_elements_by_id('pass')
        pass_word[0].send_keys('lockcapsscroll2304')
        button_login = self.driver.find_elements_by_id('u_0_1')
        button_login[0].click()
        button_check_point = self.driver.find_elements_by_id('checkpointSubmitButton')
        button_check_point[0].click()

    def post(self):
        driver = self.driver
        import pdb; pdb.set_trace()
        try:
            post_button = driver.find_element_by_id("post_button")
            post_button.click()
        except:
            sleep(2)
            post_button = driver.find_element_by_id("post_button")
            post_button.click()

        #add tag
        tag_info= driver.find_element_by_id('month')
        tag_info.click()
        tag_info.send_keys('c')
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
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.edited_question_info_detail))
        submit_button = driver.find_element_by_id('submit_button')
        submit_button.click()

    """
    def testLikeUnlikeAtQuestionList(self):
        driver = self.driver
        self.post()
        import pdb; pdb.set_trace()
        question_list_button = self.driver.find_element_by_id('logo_site')
        question_list_button.click()
        question_one = self.driver.find_element_by_class_name('article_header')
        """


    def testPostEditDelete(self):
        """
         write more in one testcase to reduce the login activity
        """
        driver = self.driver
        self.post()
        #confirm the posted question
        question_info_result = driver.find_element_by_class_name('article_header')
        import pdb;pdb.set_trace()
        self.assertIn(question_info_result.text, self.question_info)
        self.edit_post()
        question_info_result = driver.find_element_by_class_name('article_header')
        self.assertIn(question_info_result.text, self.edit_question_info)
        self.delete_post()
        #check the url
        url_info = driver.current_url
        self.assertIn(url_info, BASE_URL + 'question_list')
        #go to profile




    def tearDown(self):
        self.driver.close()


class TestUnLogginUserVisitPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)
        self.answer_button_text = 'tra loi'
        self.answer_text   = 'quan diem'
    def testQuestionPage(self):
        question_list_button = self.driver.find_element_by_id('logo_site')
        question_list_button.click()
        question_one = self.driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()
        #check if no answer button is there
        try:
            self.driver.find_element_by_id('inputCommentButton')
            return True
        except NoSuchElementException:
            pass
        #click on writer of question
        user_profile = self.driver.find_element_by_id('user_profile')
        user_profile.click()
        self.driver.back()
        #click on  question on right side bar
        side_bar_questions = self.driver.find_element_by_id('right_bar_question_list')
        question = side_bar_questions.find_element_by_id('related_question')
        question.click()


    def testVisitUserProfile(self):
        #go back
        question_list_button = self.driver.find_element_by_id('logo_site')
        question_list_button.click()
        #click on popularity panel
        user_profile = self.driver.find_element_by_id('user_profile')
        user_profile.click()
        #back
        self.driver.back()
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
suite.addTest(unittest.makeSuite(TestPostNewArticle))
#suite.addTest(unittest.makeSuite(TestUserProfile))
suite.addTest(unittest.makeSuite(TestUnLogginUserVisitPage))
unittest.TextTestRunner(verbosity=2).run(suite)
