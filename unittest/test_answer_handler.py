__author__ = 'huyheo'

import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())


class TestAnswerHandling(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = "tag1"
        self.question_id = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question()

    def _create_an_answer(self, answer_info):
        answer_id = answer_handler().add_to_answer_tbl(self.question_id, answer_info, auth.user.id)
        return answer_id
    def _add_value_of_answer_to_request(self,answer_id, question_id, answer_info):
        if answer_id:
            request.vars.answer_id = answer_id
        if question_id:
            request.vars.question_id = question_id
        request.vars.answer_info = answer_info

    def testPostNewAnswer(self):
        answer_info = "this is an answer"
        self._add_value_of_answer_to_request(None,self.question_id, answer_info)
        answer_id = create_new_answer(request, auth)
        self.assertEqual(type(answer_id), gluon.dal.Reference)
    def testUpdateAnAnswer(self):
        answer_id = self._create_an_answer("this is an answer")
        answer_update_info = "this is updated answer"
        self._add_value_of_answer_to_request(answer_id,None, answer_update_info)
        user_update_an_answer()
        #query answer
        answer_record = db(db.answer_tbl.id == answer_id).select()[0]
        self.assertEqual(answer_record.answer_info, answer_update_info)









suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAnswerHandling))
unittest.TextTestRunner(verbosity=2).run(suite)


