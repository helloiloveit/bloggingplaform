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











suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUserTagHandler))
unittest.TextTestRunner(verbosity=2).run(suite)


