__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testUnloginUser.py

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

def click_like_unlike_button(like_button):
    color = like_button.value_of_css_property('color')
    import pdb; pdb.set_trace()
    if color =='rgba(128, 128, 128, 1)':
    #not like this button yet
        like_button.click()
        sleep(2)
        color = like_button.value_of_css_property('color')
        if color == 'rgba(207, 9, 9, 1)':
            return True
    elif color == 'rgba(207, 9, 9, 1)':
        # already liked
        like_button.click()
        sleep(2)
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


class TestRattingQuestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.driver.get(QUESTION_LIST_URL)

    def testLikeaQuestion(self):
        """
        view each question in question_list once by onec
        """
        def like_unlike_question(question_list,i):
            question_unit = question_list[i].find_element_by_class_name('article_popularity_info')
            like_button = question_unit.find_element_by_class_name('like_unlike_button')
            #check if its clicked or not using color
            rst = click_like_unlike_button(like_button)
            self.assertTrue(rst)

        question_list = self.driver.find_elements_by_xpath('//table[@class="content_list_table"]//tbody//tr[@class="article_unit"]')
        for i in range(0, len(question_list),1):
            like_unlike_question(question_list,i)


    def tearDown(self):
        self.driver.close()


class TestHandlingAnswer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        user_login(self.driver)
        self.answer_info = 'this is an answer'
        self.answer_edit_info = 'this is an answer'
        self.driver.get(QUESTION_LIST_URL)
        question_one = self.driver.find_element_by_class_name('article_header')
        link = question_one.find_element_by_link_text(question_one.text)
        link.click()

    def postAnswer(self):
        import pdb;pdb.set_trace()
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
        import pdb; pdb.set_trace()
        edit_button = handling_info.find_element_by_id('edit_answer_button')
        edit_button.click()
        sleep(3)
        self.driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        self.driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.answer_edit_info))
        submit_button= self.driver.find_element_by_id('post_answer_button')
        submit_button.click()
        pass

    def AnswerElement(self, answer_info):
        import pdb; pdb.set_trace()
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

    def LikeUnLikeFunction(self, answer_info):
        handling_info = answer_info.find_element_by_class_name('article_popularity_info')
        like_button = handling_info.find_element_by_class_name('like_unlike_button')
        rst = click_like_unlike_button(like_button)
        self.assertTrue(rst)


    def testHandlingAnswer(self):
        # check number of answer available
        # to do : user another test user to create answer then test with it.  onwer of answer and not owner of answer
        popularity_info = self.driver.find_element_by_class_name('article_popularity_info')
        info = popularity_info.text.split(' ')
        if info[0] == '0':
            #no answer
            self.postAnswer()

        answer_area = self.driver.find_element_by_class_name("article_comment_container")
        self.AnswerElement(answer_area)
        self.LikeUnLikeFunction(answer_area)
        """
        self.editAnswer(handling_info)
        answer_area = self.driver.find_element_by_class_name("article_comment_container")
        handling_info = answer_area.find_element_by_class_name('article_popularity_info')
        self.deleteAnswer(handling_info)
        """
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
            import pdb; pdb.set_trace()

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
            sleep(3)
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
        self.assertIn( BASE_URL + 'question_list',url_info)
        #go to profile




    def tearDown(self):
        self.driver.close()





suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAuth))
suite.addTest(unittest.makeSuite(TestHandlingQuestion))
suite.addTest(unittest.makeSuite(TestHandlingAnswer))
suite.addTest(unittest.makeSuite(TestRattingQuestion))
suite.addTest(unittest.makeSuite(TestUserProfile))
unittest.TextTestRunner(verbosity=2).run(suite)
