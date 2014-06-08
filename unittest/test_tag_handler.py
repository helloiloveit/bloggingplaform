__author__ = 'huyheo'
import os
file_path = os.path.join(os.getcwd(),'applications','welcome','unittest','setup_test.py')
execfile(file_path, globals())


class TestTagHandling(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()

    def testUserPostNewTag(self):
        new_tag = 'new_tag'
        request.vars.tag_info = new_tag
        tag_handler()
        #query new tag
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()[0]
        self.assertEqual(record.name, new_tag.capitalize())
    def testUserPostExistedTag(self):
        self.testUserPostNewTag()
        new_posted_tag = 'new_tag'
        request.vars.tag_info = new_posted_tag
        tag_handler()
        #confirm that there's only one tag with the name
        record = db(db.tag_tbl.name == request.vars.tag_info.capitalize()).select()
        self.assertTrue(len(record) == 1)











suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTagHandling))
unittest.TextTestRunner(verbosity=2).run(suite)


