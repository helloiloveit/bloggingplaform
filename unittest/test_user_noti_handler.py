__author__ = 'huyheo'



import os
import mock
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())
from noti_handler import *

class noti_handler_fake_queue(noti_handler):
    def add_to_gae_task_queue(self):
        """
        cant call function in default.py by import it
        so to make Mock test easy ..call handler_fb_noti
        """
        request.vars['question_id'] = self.question_id
        handler_fb_noti(request)


class QuestionHandlingUtilityTestNoti(QuestionHandlingUtility):
    """
    because Noti need gae task handler :
    Create a question then make a call to noti manually for testing
    """
    def create_a_question(self):
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)
        if question_id:
            noti_handler_fake_queue(question_id).add_to_gae_task_queue()
        return question_id

class TestNotiWhenUserMakeQuestion(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        # question info
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = ""

    def save_tag_info_for_user(self, tag_info, user_info):
        auth.user = user_info
        self.tag_list = tag_info
        save_tag_info_for_user(tag_info, auth)


    @mock.patch('noti_handler.fb_noti_handler')
    def testUserPostQuestionWithTagOfHimSelf(self, mock_fb_noti):
        self.save_tag_info_for_user("tag1", auth.user)
        question_id = QuestionHandlingUtilityTestNoti(self.question, self.question_detail_info, self.tag_list).create_a_question()
        href_link = noti_handler(question_id).create_href()
        mock_fb_noti.assert_called_with(auth.user.username, href_link, self.question)

    @mock.patch('noti_handler.fb_noti_handler')
    def testUserPostQuestionWithTagOfOther(self, mock_fb_noti):
        self.save_tag_info_for_user("tag1", user_record_2)
        question_id = QuestionHandlingUtilityTestNoti(self.question, self.question_detail_info, self.tag_list).create_a_question()
        href_link = noti_handler(question_id).create_href()
        mock_fb_noti.assert_called_with(auth.user.username, href_link, self.question)

    @mock.patch('noti_handler.fb_noti_handler')
    def testUserPostQuestionWithTagOfOthers(self, mock_fb_noti):
        self.save_tag_info_for_user("tag1", user_record_2)
        self.save_tag_info_for_user("tag1", user_record_3)

        question_id = QuestionHandlingUtilityTestNoti(self.question, self.question_detail_info, self.tag_list).create_a_question()
        href_link = noti_handler(question_id).create_href()
        mock_fb_noti.assert_any_call(user_record_3.username, href_link, self.question)
        mock_fb_noti.assert_any_call(user_record_2.username, href_link, self.question)

    @mock.patch('noti_handler.fb_noti_handler')
    def testUserPostQuestionWithTagOption1(self, mock_fb_noti):
        self.save_tag_info_for_user("tag1", user_record_1)
        self.save_tag_info_for_user("tag1", user_record_2)
        self.save_tag_info_for_user("tag1", user_record_3)

        question_id = QuestionHandlingUtilityTestNoti(self.question, self.question_detail_info, self.tag_list).create_a_question()
        href_link = noti_handler(question_id).create_href()
        mock_fb_noti.assert_any_call(user_record_1.username, href_link, self.question)
        mock_fb_noti.assert_any_call(user_record_2.username, href_link, self.question)
        mock_fb_noti.assert_any_call(user_record_3.username, href_link, self.question)








suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestNotiWhenUserMakeQuestion))
unittest.TextTestRunner(verbosity=2).run(suite)


