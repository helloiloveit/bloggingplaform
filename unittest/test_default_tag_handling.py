
__author__ = 'huyheo'

import os
import mock
from gluon import *
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
        SyntaxError: Non-ASCII character '\xe1' in file applications/chuotnhat/unittest/test_user_tag_handler.py
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
        self.tag_info = u'\u0111i ch\u01a1i kh\xf4nng'
        request.vars.tag_info = self.tag_info
        create_new_tag()
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()[0]
        unicode_tag = unicode(record.name, "utf-8")
        self.assertEqual(unicode_tag, self.tag_info.capitalize())

    def testCreateNewTagWithCaptitalNotAtStart(self):
        self.tag_info = u'\u0111i Ch\u01a1i kh\xf4ng'
        request.vars.tag_info = self.tag_info
        create_new_tag()
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()[0]
        unicode_tag = unicode(record.name, "utf-8")
        self.assertEqual(unicode_tag, self.tag_info.capitalize())

    def testCreateNewTagWithCaptitalAtStart(self):
        self.tag_info = u'\u0110i ch\u01a1i kh\xf4ng'
        request.vars.tag_info = self.tag_info
        create_new_tag()
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()[0]
        unicode_tag = unicode(record.name, "utf-8")
        self.assertEqual(unicode_tag, self.tag_info.capitalize())

    def checkDuplicateTag(self, valid_tag, invalid_tag, first_letter_flag):
        request.vars.tag_info = valid_tag
        create_new_tag()
        # di choi khong
        request.vars.tag_info = invalid_tag
        create_new_tag()
        #query
        record = db(db.tag_tbl.name == valid_tag).select()
        self.assertEqual(len(record), 1)
        unicode_tag = unicode(record[0].name, "utf-8")
        self.assertEqual(unicode_tag, valid_tag )

        if first_letter_flag:
            record = db(db.tag_tbl.name == invalid_tag.capitalize()).select()
            self.assertEqual(len(record), 1)
        else:
            record = db(db.tag_tbl.name == invalid_tag).select()
            with self.assertRaises(IndexError):
                record[0]

            check_name = invalid_tag[0].upper() + invalid_tag[1:]
            record = db(db.tag_tbl.name == check_name).select()
            with self.assertRaises(IndexError):
                record[0]


    def testDuplicateTagByCapitalLetterFirstLetter(self):
        # Di choi khong
        tag_1 = u'\u0110i ch\u01a1i kh\xf4ng'
        # di choi khong
        tag_2 = u'\u0111i ch\u01a1i kh\xf4ng'
        self.checkDuplicateTag(tag_1, tag_2, True)

    def testDuplicateTagByCapitalLetterPositionRandom(self):
        # Di choi khong
        valid_tag = u'\u0110i ch\u01a1i kh\xf4ng'
        # di Choi khong
        invalid_tag = u'\u0111i Ch\u01a1i kh\xf4ng'
        self.checkDuplicateTag(valid_tag, invalid_tag, False)

    def testDuplicateTagByCapitalLetterPositionRandom_last(self):
        # Di choi khong
        valid_tag = u'\u0110i ch\u01a1i kh\xf4ng'
        # di choi Khong
        invalid_tag = u'\u0111i ch\u01a1i Kh\xf4ng'
        self.checkDuplicateTag(valid_tag, invalid_tag, False)



    def testUserPostNewTag(self):
        """
        user post new tag
        """
        request.vars.tag_info = self.tag_info
        return_info = tag_handler()
        pass

class TagCreateUtility(object):
    def generate_tag_list(self, length):
        tag_list = []
        for i in range(0, length, 1):
            tag_list.append('tag'+ str(i))
        return tag_list

    def capitalize_tag_list(self, tag_info):
        for i in range(0,len(tag_info),1):
            tag_info[i] = tag_info[i].title()
        return tag_info


    def create_new_tag(self, tag_info):
        for tag in tag_info:
            request.vars.tag_info = tag
            create_new_tag()

class HandleTagList(object):
    """
    cant be use as standalone object.
    Need to be subclass by a Test clase for initializing request, tag_utility
    """
    def check_update_new_tag_list(self, tag_info):
        self.tag_utility.create_new_tag(tag_info)
        request.vars.update({'tag_info[]': tag_info})
        fb_save_tag_list()
        html_return = fb_main()
        self.assertEqual(html_return['tag_list'], tag_info)

    def check_update_old_tag_list(self, tag_info):
        request.vars.update({'tag_info[]': tag_info})
        fb_save_tag_list()
        html_return = fb_main()
        self.assertEqual(html_return['tag_list'], tag_info)


class TestFbMainUpdateTag(unittest.TestCase, HandleTagList):
    def setUp(self):
        set_up_basic_environment()
        self.tag_utility = TagCreateUtility()
        pass

    def testUserUpdateNewTagInfo1(self):
        tag_info = ['Tag1', 'Tag2']
        self.check_update_new_tag_list(tag_info)
        tag_info = ['Tag1']
        self.check_update_new_tag_list(tag_info)

    def testUserUpdateEmptyTagList(self):
        tag_info = ['Tag1', 'Tag2']
        self.check_update_new_tag_list(tag_info)
        request.vars.update({'tag_info[]': None})
        fb_save_tag_list()
        html_return = fb_main()
        self.assertEqual(html_return['tag_list'], [])


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


    def testDuplicate(self):
        tag_list = self.tag_utility.generate_tag_list(40)
        self.check_update_new_tag_list(tag_list)
        new_tag_list = tag_list[:10]
        self.check_update_new_tag_list(new_tag_list)
        new_tag_list = tag_list[3:10]
        self.check_update_old_tag_list(new_tag_list)
        new_tag = tag_list[3]
        self.check_update_new_tag_list([new_tag])



class TestCreateNewTag(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_utility = TagCreateUtility()

    def testDuplicateTag(self):
        tag_list = self.tag_utility.generate_tag_list(30)

        self.tag_utility.create_new_tag(tag_list)
        self.tag_utility.capitalize_tag_list(tag_list)
        query_tag_list = tag_tbl_handler().get_all_tag_info_from_db()
        self.assertEqual(tag_list, query_tag_list)

        tag_list_new = tag_list[:10]
        self.tag_utility.create_new_tag(tag_list)
        query_tag_list = tag_tbl_handler().get_all_tag_info_from_db()
        self.assertEqual(tag_list, query_tag_list)




class TestFbQuestionList(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.tag_utility = TagCreateUtility()

    def testLoadEmptySite(self):
        html_return = fb_question_list()
        pass

    def testLoadSiteWithInfo(self):
        pass

class TestFbMainNoti(unittest.TestCase, HandleTagList):
    """
    question?id=5404831942443008&fb_source=notification&ref=notif&notif_t=app_notificatio
    <Storage {'fb_source': 'notification', 'notif_t': 'app_notification', 'ref': 'notif', 'id': '5404831942443008'}>
    """
    def setUp(self):
        set_up_basic_environment()
        self.tag_utility = TagCreateUtility()

    @mock.patch('http.redirect')
    def LoadByNoti(self, mock_redirect):
        """
        redirect is imported by default though gluon
        so if we need to find a way to import default.gluon

        """
        tag_info = ['Tag1', 'Tag2']
        self.check_update_new_tag_list(tag_info)
        self.question_id = QuestionHandlingUtility('question header','question detail','tag1').create_a_question()
        request.vars.update({ 'fb_source': 'notification'})
        request.vars.update({  'notif_t': 'app_notification'})
        request.vars.update({ 'id':self.question_id})
        request.vars.function = 'question'
        html_dic = fb_main()
        mock_redirect.return_value = ''
        mock_redirect.assert_called_with('', '', '')

        pass





suite = unittest.TestSuite()
"""
suite.addTest(unittest.makeSuite(TestFbMainUpdateTag))
suite.addTest(unittest.makeSuite(TestCreateNewTag))
suite.addTest(unittest.makeSuite(TestFbQuestionList))
"""
suite.addTest(unittest.makeSuite(TestTagHandling))
#suite.addTest(unittest.makeSuite(TestFbMainNoti))
unittest.TextTestRunner(verbosity=2).run(suite)






