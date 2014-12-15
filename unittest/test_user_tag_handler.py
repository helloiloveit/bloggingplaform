__author__ = 'huyheo'



import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())

execfile(os.path.join(file_path,'modules','tag_handler.py'), globals())



class TestUserTagHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_list = ['tag1','tag2','tag3']
        self.tag_list2 = ['tag4', 'tag5', 'tag6']


    def testCreateTagList(self):
        user_tag_handler(auth).create_tag_list(self.tag_list)
        record = db(db.user_tag_tbl.user_info == auth.user.id).select()
        tag_name_list = tag_tbl_handler().get_name_list_from_record_list(record)
        self.assertEqual(tag_name_list, self.tag_list)

    def testUpdateNewTagList(self):
        self.testCreateTagList()
        user_tag_handler(auth).update_new_tag_list(self.tag_list2)
        record = db(db.user_tag_tbl.user_info == auth.user.id).select()
        tag_name_list = tag_tbl_handler().get_name_list_from_record_list(record)
        self.assertEqual(tag_name_list, self.tag_list2)

    def testUpdateNoneTagList(self):
        self.testCreateTagList()



    def testGetTagInfo(self):
        self.tag_list = ['tag1']
        user_tag_handler(auth).create_tag_list(self.tag_list)
        query_tag_list = user_tag_handler(auth).get_tag_info()
        self.assertEqual(self.tag_list, query_tag_list)

    def testGetTagInfo2(self):
        self.tag_list = ['tag1', 'tag2']
        user_tag_handler(auth).create_tag_list(self.tag_list)
        query_tag_list = user_tag_handler(auth).get_tag_info()
        self.assertEqual(self.tag_list, query_tag_list)

    def testGetTagInfo3(self):
        self.tag_list = ['tag1','tag2', 'tag3']
        user_tag_handler(auth).create_tag_list(self.tag_list)
        query_tag_list = user_tag_handler(auth).get_tag_info()
        self.assertEqual(self.tag_list, query_tag_list)





class TestQuestionTagHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_info = "tag1,tag2,tag3"
        self.tag_list = self.tag_info.split(',')
        self.questionUtitlity = QuestionHandlingUtility('question header', 'questiondetail',self.tag_info)
    """
    def test_get_question_by_tag(self):
        import pdb; pdb.set_trace()
        question_id = self.questionUtitlity.create_a_question()
        user_tag_handler(auth).create_tag_list(self.tag_list[0])
        tag_id_list = tag_tbl_handler().get_id_list_from_tag_name_list(self.tag_list)
        question_list = question_tag_handler().get_question_by_tag(tag_id_list)
        question_record = db(db.question_tbl.id == question_id).select()
        self.assertTrue(question_record in question_list )
        pass
        """





suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUserTagHandler))
suite.addTest(unittest.makeSuite(TestQuestionTagHandler))
unittest.TextTestRunner(verbosity=2).run(suite)


