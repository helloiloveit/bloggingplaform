__author__ = 'huyheo'

#python web2py.py -S welcome -M -R applications/welcome/funtionalTest/testPostQuestion.py

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
BASE_URL = "http://localhost:8002/"
LOGIN_URL = "http://localhost:8002/user/login?_next=/"
LOGOUT_URL = "http://localhost:8002/user/logout?_next=/"


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def user_login(self):
        self.driver.get(LOGIN_URL)

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
        self.driver.get(LOGIN_URL)
        self.question_info = 'this is a question'
        self.edit_question_info = 'this is a edited question'
        self.question_info_detail = ' this is a detail of question'
        self.edited_question_info_detail = ' this is a detail of question'

    def post(self):
        driver = self.driver
        post_button = driver.find_element_by_id("post_button")
        post_button.click()
        #add tag
        tag_info= driver.find_element_by_id('month')
        tag_info.send_keys('tag1')
        post_tag_button = driver.find_element_by_id('submit1')
        post_tag_button.click()
        #add question title
        question_info = driver.find_element_by_id('question_info')
        question_info.clear()
        question_info.send_keys(self.question_info)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.question_info_detail))
        submit_button = driver.find_element_by_id('submit_button')
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
        question_info = driver.find_element_by_id('question_info')
        question_info.clear()
        question_info.send_keys(self.edit_question_info)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.edited_question_info_detail))
        submit_button = driver.find_element_by_id('submit_button')
        submit_button.click()



    def testPostEditDelete(self):
        """
         write more in one testcase to reduce the login activity
        """
        import pdb;pdb.set_trace()
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
        self.assertIn(url_info, BASE_URL + 'question_list')
        #go to profile
    """
    def testEdit(self):
        import pdb;pdb.set_trace()
        driver = self.driver
        self.post()
        self.edit_post()
        #confirm the edit result
        question_info_result = driver.find_element_by_class_name('article_header')
        self.assertIn(question_info_result.text, self.edit_question_info)
    """




    def tearDown(self):
        self.driver.close()



suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestAuth))
#suite.addTest(unittest.makeSuite(TestPostNewArticle))
suite.addTest(unittest.makeSuite(TestUserProfile))
unittest.TextTestRunner(verbosity=2).run(suite)
