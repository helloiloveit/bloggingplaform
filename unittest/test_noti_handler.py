__author__ = 'huyheo'



import os
import mock
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())

execfile(os.path.join(file_path,'modules','noti_handler.py'), globals())



class TestNotiHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        # question info
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = "tag1"
    """
    def testSendFbNoti(self):
        fb_noti_handler(self.user_id, self.href, self.message).send()
    """
    def automate_checking(self, tag_list, user_list):
        # post question with two tag --> noti 2 user
        self.tag_list = tag_list
        question_id_3 = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question_by_user(auth)
        user_data = noti_handler(question_id_3).get_targeted_user()
        rst_user_list = []
        for temp in user_data:
            user_record = db(db.auth_user.id == temp.user_info).select()[0]
            rst_user_list.append(user_record.username)
        self.assertEqual(rst_user_list, user_list)


    def testAddToGaeTaskQueue(self):
        question_id = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question()
        request.vars.update({'question_id': question_id})
        add_gae_queue()

    def testGetTargetedUser(self):
        save_tag_info_for_user(self.tag_list, auth)
        user_list = [user_record_1.username]
        self.automate_checking(self.tag_list, user_list)


    def testGetMultipleTargetedUser(self):


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
        self.automate_checking(self.tag_list, user_list)


        self.tag_list = "tag1"
        user_list = [user_record_1.username]
        self.automate_checking(self.tag_list, user_list)


        self.tag_list = "tag2,tag3"
        user_list = [user_record_2.username, user_record_3.username]
        self.automate_checking(self.tag_list, user_list)

        # 3 tags
        self.tag_list = "tag1,tag2,tag3"
        user_list = [user_record_1.username, user_record_2.username, user_record_3.username]
        self.automate_checking(self.tag_list, user_list)
        pass

    def testSameTag(self):
        #create 1 first question
        auth.user = user_record_2
        self.tag_list = "tag1"
        save_tag_info_for_user(self.tag_list, auth)
        auth.user = user_record_3
        self.tag_list = "tag1"
        save_tag_info_for_user(self.tag_list, auth)

        # post question with two tag --> noti 2 user
        self.tag_list = "tag1"
        user_list = [user_record_2.username, user_record_3.username]
        self.automate_checking(self.tag_list, user_list)











suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestNotiHandler))
unittest.TextTestRunner(verbosity=2).run(suite)


