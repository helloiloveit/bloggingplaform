
__author__ = 'huyheo'

import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())






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

class TestUpdateTagInfo(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()

    def check_update_new_tag_list(self, tag_info):
        for tag in tag_info:
            request.vars.tag_info = tag
            create_new_tag()
        request.vars.update({'tag_info[]': tag_info})
        fb_save_tag_list()
        html_return = fb_main()
        self.assertEqual(html_return['tag_list'], tag_info)

    def check_update_old_tag_list(self, tag_info):
        request.vars.update({'tag_info[]': tag_info})
        fb_save_tag_list()
        html_return = fb_main()
        self.assertEqual(html_return['tag_list'], tag_info)



    def testUserUpdateNewTagInfo1(self):
        tag_info = ['Tag1', 'Tag2']
        self.check_update_new_tag_list(tag_info)
        tag_info = ['Tag1']
        self.check_update_new_tag_list(tag_info)

    def testUserUpdateNewTagInfo2(self):
        tag_info = ['Tag1', 'Tag2']
        self.check_update_new_tag_list(tag_info)
        tag_info = ['Tag1', 'Tag2', 'Tag3']
        self.check_update_new_tag_list(tag_info)

    def testUserUpdateNewTagInfo3(self):
        tag_info = []
        self.check_update_new_tag_list(tag_info)
        tag_info = ['Tag1', 'Tag2', 'Tag3']
        self.check_update_new_tag_list(tag_info)


    def testUserUpdateEmptyTag(self):
        tag_info = []
        self.check_update_new_tag_list(tag_info)


    def testUserChangeTagList(self):
        tag_info = ['Tag1', 'Tag2', 'Tag3']
        self.check_update_new_tag_list(tag_info)
        tag_info = ['Tag2', 'Tag3']
        self.check_update_old_tag_list(tag_info)











suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUpdateTagInfo))
unittest.TextTestRunner(verbosity=2).run(suite)






