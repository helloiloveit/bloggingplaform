__author__ = 'huyheo'

import os
file_path = os.path.join(os.getcwd(),'applications','welcome','unittest','setup_test.py')
execfile(file_path, globals())



class TestQuestionHandling(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()

    def _add_value_of_question_to_request(self,question_id,question, question_detail_info):
        request.vars.question_info = question
        request.vars.editor1 = question_detail_info
        if question_id:
            request.vars.question_id = question_id
    @classmethod
    def _create_a_question(self):
        question = "this is a new question"
        question_detail_info = "more detail of this question"
        question_id = question_handler(None,question, question_detail_info, auth.user.id).create_new_record_in_question_tbl()
        return question_id


    def testPostNewQuestion(self):
        #set variable for the test
        question = "this is a new question"
        question_detail_info = "more detail of this question"
        self._add_value_of_question_to_request(None,question,question_detail_info)
        question_id = post_new_question(request, auth)
        #update_to_question_tbl('','', auth.user.id)
        self.assertEqual(type(question_id),gluon.dal.Reference)

    def testUpdateOldQuestion(self):
        #create a question in db
        question_id = self._create_a_question()
        #update
        question = "this is an updated question"
        question_detail_info = "update more detail of this question"
        self._add_value_of_question_to_request(question_id, question,question_detail_info )
        user_modify_question()
        #get the question
        question_record = db(db.question_tbl.id == question_id).select()[0]
        self.assertEqual(question_record.question_info , question)
        self.assertEqual(question_record.question_detail_info , question_detail_info)

    def testDeleteAQuestion(self):
        #create a question in db
        question_id = self._create_a_question()
        #delete that question
        request.args[0] = question_id
        user_delete_question()
        #query that question
        question = db(db.question_tbl.id == question_id).select()
        with self.assertRaises(IndexError):
            question[0]



class TestQuestionRattingHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self._question_id = TestQuestionHandling._create_a_question()
        #create second user as audience
        user_id =  db.auth_user.insert(first_name = 'audience', email = 'audienceemail@gmail.com')
        self._audience = db(db.auth_user.id == user_id).select()[0]



    def testLikeAQuestion(self):

        #check if audience is in like list of question
        def check_if_user_did_like_question():
            question_like_record = db((db.question_like_tbl.question_id == self._question_id)&(db.question_like_tbl.user_info == self._audience.id )).select()
            return question_like_record
        question_like_record = check_if_user_did_like_question()

        with self.assertRaises(IndexError):
            question_like_record[0]

        #make a like
        owner_of_question = auth.user
        auth.user = self._audience
        request.vars.question_id = self._question_id
        user_like_a_question()

        #check if audience is in like-list of question
        question_like_record = check_if_user_did_like_question()
        self.assertEqual(type(question_like_record[0].id),long)
        pass

    def testDisLikeAQuestion(self):
        #make a like
        self.testLikeAQuestion()

        #make a unlike
        owner_of_question = auth.user
        auth.user = self._audience
        request.vars.question_id = self._question_id
        user_unlike_a_question()
        #check if audience is not in like-list of question
        def check_if_user_did_like_question():
            question_like_record = db((db.question_like_tbl.question_id == self._question_id)&(db.question_like_tbl.user_info == self._audience.id )).select()
            return question_like_record
        question_like_record = check_if_user_did_like_question()
        with self.assertRaises(IndexError):
            question_like_record[0]

    def testFollowAQuestion(self):
        pass






suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestQuestionHandling))
suite.addTest(unittest.makeSuite(TestQuestionRattingHandler))
unittest.TextTestRunner(verbosity=2).run(suite)






