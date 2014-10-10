__author__ = 'huyheo'



import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())

execfile(os.path.join(file_path,'modules','noti_handler.py'), globals())

class noti_handler_fake( noti_handler):
    def add_to_gae_task_queue(self):
        return



class TestNotiHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.user_id = "540428388"
        self.href = "huyheo"
        self.message= "what a beautiful day"
    def testSendFbNoti(self):
        noti_handler("question_id").send_fb_noti(self.user_id, self.href, self.message)

    def testAddToGaeTaskQueue(self):











suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestNotiHandler))
unittest.TextTestRunner(verbosity=2).run(suite)


