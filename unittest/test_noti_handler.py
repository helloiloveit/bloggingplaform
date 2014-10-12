__author__ = 'huyheo'



import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())

execfile(os.path.join(file_path,'modules','noti_handler.py'), globals())


class noti_handler_fake_queue( noti_handler):
    def add_to_gae_task_queue(self):
        request.vars['question_id'] = self.question_id
        add_gae_queue()

class QuestionHandlingUtilityTestNoti(QuestionHandlingUtility):
    def create_a_question(self):
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)
        if question_id:
            noti_handler_fake_queue(question_id).add_to_gae_task_queue()
        return question_id

class TestPostQuestionNoti(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        # question info
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = "tag1"
    def testPostQuestion(self):
        QuestionHandlingUtilityTestNoti(self.question, self.question_detail_info, self.tag_list).create_a_question()





class TestNotiHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.user_id = "540428388"
        self.href = "huyheo"
        self.message= "what a beautiful day"
        # question info
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = "tag1"
    """
    def testSendFbNoti(self):
        fb_noti_handler(self.user_id, self.href, self.message).send()
    """

    def testAddToGaeTaskQueue(self):
        question_id = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question()
        request.vars.update({'question_id': question_id})
        add_gae_queue()

    def testGetTargetedUser(self):
        question_id = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question()
        save_tag_info_for_user(self.tag_list, auth)
        user_data = noti_handler(question_id).get_targeted_user()
        user_record = db(db.auth_user.id == user_data[0][0].user_info).select()[0]
        self.assertEqual(user_record.username, auth.user.username)


    def testGetMultipleTargetedUser(self):
        def test_with_level(tag_list, user_list):
            # post question with two tag --> noti 2 user
            self.tag_list = tag_list
            question_id_3 = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question_by_user(auth)
            user_data = noti_handler(question_id_3).get_targeted_user()
            rst_user_list = []
            for temp in user_data:
                user_record = db(db.auth_user.id == temp.first().user_info).select()[0]
                rst_user_list.append(user_record.username)
            self.assertEqual(rst_user_list, user_list)


        #create 1 first question
        auth.user = user_record_1
        self.tag_list = "tag1"
        save_tag_info_for_user(self.tag_list, auth)
        auth.user = user_record_2
        self.tag_list = "tag2"
        save_tag_info_for_user(self.tag_list, auth)
        auth.user = user_record_3
        self.tag_list = "tag3"
        save_tag_info_for_user(self.tag_list, auth)

        # post question with two tag --> noti 2 user
        self.tag_list = "tag1,tag2"
        user_list = [user_record_1.username, user_record_2.username]
        test_with_level(self.tag_list, user_list)


        self.tag_list = "tag1"
        user_list = [user_record_1.username]
        test_with_level(self.tag_list, user_list)

        # 3 tags
        self.tag_list = "tag1,tag2,tag3"
        user_list = [user_record_1.username, user_record_2.username, user_record_3.username]
        test_with_level(self.tag_list, user_list)
        pass













suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestNotiHandler))
unittest.TextTestRunner(verbosity=2).run(suite)


