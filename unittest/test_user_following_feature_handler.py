__author__ = 'huyheo'
import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())


class TestTagHandling(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        #set up user to follow
        person_id =  db.auth_user.insert(first_name = 'user_to_follow')
        self.target_person = db(db.auth_user.id == person_id).select()[0]

    def testFollowAUser(self):
        request.vars.person_id = self.target_person.id
        user_follow_a_person(request, auth)
        #confirm target person is followed
        record = db((db.follow_info_tbl.followed_user == self.target_person.id)&(db.follow_info_tbl.following_user == auth.user.id )).select()
        self.assertEqual(len(record), 1)

    def testFollowMe(self):
        self.target_person = auth.user
        request.vars.person_id = auth.user
        user_follow_a_person(request, auth)
        #confirm target person is followed
        record = db((db.follow_info_tbl.followed_user == self.target_person.id)&(db.follow_info_tbl.following_user == auth.user.id )).select()
        self.assertEqual(len(record), 1)

    def testUnFollowAUser(self):
        request.vars.person_id = self.target_person.id
        user_follow_a_person(request, auth)
        user_unfollow_a_person(request, auth)
        #confirm target person is unfollowed
        record = db((db.follow_info_tbl.followed_user == self.target_person.id)&(db.follow_info_tbl.following_user == auth.user_id )).select()
        self.assertEqual(len(record), 0)









suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTagHandling))
unittest.TextTestRunner(verbosity=2).run(suite)


