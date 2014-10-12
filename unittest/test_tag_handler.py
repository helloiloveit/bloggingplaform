__author__ = 'huyheo'



import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())

execfile(os.path.join(file_path,'modules','tag_handler.py'), globals())

class TestTagHandling(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_info = 'new_tag'
        self.div_id = "suggestion_box"

    def createReturnHtmlForAddingNewTag(self):
        """
        SyntaxError: Non-ASCII character '\xe1' in file applications/chuotnhat/unittest/test_tag_handler.py
         on line 15, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
        """
        temp = [DIV(u'',
                    _onclick="user_post_new_tag('%s','%s');" %(self.tag_info, self.div_id),
                    _onmouseover="this.style.backgroundColor='yellow'",
                    _onmouseout="this.style.backgroundColor='white'"
        )]
        return DIV(temp, _id ="%s" % self.div_id )

    def createReturnHtmlForAddingExistedTag(self, existed_tag_list):
        temp = [DIV(k,
                    _onclick="user_select_tag_handler('%s','%s');" %(k,self.div_id),
                    _onmouseover="this.style.backgroundColor='yellow'",
                    _onmouseout="this.style.backgroundColor='white'"
        ) for k in selected]
        return DIV(temp, _id ="%s" % div_id )

    def testCreateNewTag(self):
        request.vars.tag_info = self.tag_info
        create_new_tag()
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()[0]
        self.assertEqual(record.name, self.tag_info.capitalize())


    def testUserPostNewTag(self):
        """
        user post new tag
        """
        request.vars.tag_info = self.tag_info
        return_info = tag_handler()
        #self.assertEqual(return_info, self.createReturnHtmlForAddingNewTag())


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



class UserActivity(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_list = ['tag1','tag2','tag3']
        self.tag_list2 = ['tag4', 'tag5', 'tag6']

    def testUserUpdateNewTagInfo(self):
        #request.vars = {'tag_info[]': self.tag_list}
        #fb_save_tag_list()
        save_tag_info_for_user(self.tag_list, auth)
        record = db(db.user_tag_tbl.user_info == auth.user.id).select()
        tag_name_list = tag_tbl_handler().get_name_list_from_record_list(record)
        self.assertEqual(tag_name_list, self.tag_list)









suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestTagHandling))
suite.addTest(unittest.makeSuite(TestUserTagHandler))
suite.addTest(unittest.makeSuite(UserActivity))
unittest.TextTestRunner(verbosity=2).run(suite)


