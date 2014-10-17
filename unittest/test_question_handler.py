
__author__ = 'huyheo'

import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat','unittest','setup_test.py')
execfile(file_path, globals())



def create_a_question( question_info, question_detail_info, user_id, tag_list):
        question_id = question_handler().create_new(question_info,
                                                                       question_detail_info,
                                                                       user_id,
                                                                       tag_list)
        return question_id



class noti_handler( noti_handler):
    def add_to_gae_task_queue(self):
        return


class TestQuestionHandling(unittest.TestCase, QuestionHandlingUtility):
    def setUp(self):
        set_up_basic_environment()
        self.question = "this is a new question"
        self.question_detail_info = "more detail of this question"
        self.tag_list = "tag1,tag2,tag3"
        self.tag_list_list = self.tag_list.split(',')

    def testPostNewQuestion(self):
        #set variable for the test
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)
        question_record = db(db.question_tbl.id == question_id).select().first()
        def get_tag_name_list_from_record_list(record_list):
            tag_name_list= []
            for unit in record_list:
                tag = db(db.tag_tbl.id == unit.tag_info).select().first()
                tag_name_list.append(tag.name)
            return tag_name_list
        if question_record:
            question_tag_records = db(db.question_tag_tbl.question_info == question_record.id).select()
            tag_name_list = get_tag_name_list_from_record_list(question_tag_records)
            result = set(tag_name_list)&set(self.tag_list_list)
            self.assertEqual(len(result),len(self.tag_list_list))

        else:
            self.assertEqual(1,0)


        #update_to_question_tbl('','', auth.user.id)
        self.assertEqual(type(question_id),gluon.dal.Reference)
        self.assertEqual(question_record.question_info, self.question)
        self.assertEqual(question_record.question_detail_info, self.question_detail_info)
        return question_id

    def testUpdateOldQuestion(self):
        #create a question in db
        question_id = self.testPostNewQuestion()
        #update
        self.question = "this is an updated question"
        self.question_detail_info = "update more detail of this question"
        self.tag_list = "tag1,tag2,tag3,tag4"
        self.tag_list_list = self.tag_list.split(',')

        self.add_value_of_question_to_request(question_id)
        update_a_question(request)
        #get the question
        question_record = db(db.question_tbl.id == question_id).select()[0]
        self.assertEqual(question_record.question_info , self.question)
        self.assertEqual(question_record.question_detail_info , self.question_detail_info)
        #check tag
        tag_list = db(db.question_tag_tbl.question_info == question_id).select()
        self.assertEqual(len(tag_list), len(self.tag_list_list))



    def testDeleteAQuestion(self):
        #create a question in db
        questionUtility = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list)
        question_id = questionUtility.create_a_question()
        #delete that question
        request.args.append(question_id)
        delete_a_question(request)
        #query that question
        question = db(db.question_tbl.id == question_id).select()
        with self.assertRaises(IndexError):
            question[0]



class TestQuestionRattingHandler(unittest.TestCase):
    def setUp(self):
        set_up_basic_environment()
        #create second user as audience
        user_id =  db.auth_user.insert(first_name = 'audience', email = 'audienceemail@gmail.com')
        self._audience = db(db.auth_user.id == user_id).select()[0]
        auth.user = self._audience
        self.question = "question info"
        self.question_detail_info = "question detail"
        self.tag_list = "tag1,tag2"
        self._question_id = QuestionHandlingUtility(self.question, self.question_detail_info, self.tag_list).create_a_question()



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
        user_like_a_question(request, auth)

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
        user_unlike_a_question(request, auth)
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






