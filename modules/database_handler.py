__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)


def post_new_question(request, auth):
    question_txt = request.vars.question_info
    question_detail_txt = request.vars.editor1
    user_id = auth.user.id
    question_handler_obj = question_handler(None, question_txt,question_detail_txt, user_id)
    question_id = question_handler_obj.create_new_record_in_question_tbl()
    return question_id
def delete_a_question(request):
    question_id = request.args[0]
    question_handler_obj = question_handler(question_id, None,None, None)
    question_handler_obj.delete_record_in_question_tbl()
    return

def update_a_question(request):
    question_id = request.args[0]
    import pdb; pdb.set_trace()
    question_handler_obj = question_handler(question_id, request.vars.question_info, request.vars.question_detail_info,None)
    question_handler_obj.update_to_question_tbl()
    return





def like_a_question(request, auth):
    question_id = request.vars.question_id
    question_handler_obj = question_handler(question_id, None, None, None)
    record_id = question_handler_obj.vote_up_a_question(auth.user.id)
    return record_id

def unlike_a_question(request, auth):
    question_id = request.vars.question_id
    question_handler_obj = question_handler(question_id, None, None, None)
    result = question_handler_obj.vote_down_a_question(auth.user.id)
    return result

class question_handler(object):
    def __init__(self,
                 question_id,
                 question_info,
                 question_detail_info,
                 user_id):
        self.question_id = question_id
        self.question_info = question_info
        self.question_detail_info = question_detail_info
        self.user_id = user_id
        self.db = current.db

    def create_new_record_in_question_tbl(self):
        db = self.db
        question_id = None
        try:
            question_id = db.question_tbl.insert( question_info = self.question_info,
                                                question_detail_info = self.question_detail_info,
                                                writer = self.user_id)
            log.info(" successful create a tbl")
        except:
            log.error(' cant create tbl')
        log.info("question_id = %s",question_id)

        return question_id


    def update_to_question_tbl(self):
        db = self.db
        try:
            row = db(db.question_tbl.id == self.question_id).select().first()
            row.update_record(question_info = self.question_info,
                          question_detail_info = self.question_detail_info)
        except:
            log.error('cant update tbl')
        pass

    def delete_record_in_question_tbl(self):
        db = self.db
        db(db.question_tbl.id ==self.question_id).delete()
        pass

    def vote_up_a_question(self, audience_id):
        db = self.db
        question_like_id =None
        try:
            question_like_id = db.question_like_tbl.insert( question_id = self.question_id,
                                                            user_info = audience_id)
        except:
            log.error('cant create tbl')
        return question_like_id

    def vote_down_a_question(self, audience_id):
        db = self.db
        try:
            #check if user did like this question or not
            # if yes . delete this record
            # if no   return flag  0: success 1: db failed 2: user already not like it
            like_record = db((db.question_like_tbl.question_id == self.question_id)&(db.question_like_tbl.user_info == audience_id )).select()
            if len(like_record):
                db(db.question_like_tbl.id == like_record[0].id).delete()
                return SUCCESS_RESULT
            else:
                return DB_IS_UPDATED_ALREADY

        except:
            log.error('cant update db')
            return DB_FAILED
        return DB_FAILED

    def report_a_question(self, audience):
        db  = self.db
        question_report_id =None
        try:
            question_report_id = db.question_report_tbl.insert(question_id = self.question_id,
                                                               user_info = audience)
        except:
            log.error('cant create tbl')
        return question_report_id

########################answer #####################
def create_new_answer(request, auth):
    question_id = request.vars.question_id
    answer_info = request.vars.answer_info
    answer_id = answer_handler(None, answer_info, auth.user.id).add_to_answer_tbl(question_id)
    return answer_id

def update_an_answer(request):
    answer_id = request.vars.answer_id
    answer_info = request.vars.answer_info
    answer_handler(answer_id, answer_info, None).update_to_answer_tbl()
    pass
def del_an_answer(request):
    answer_id = request.vars.answer_id
    answer_handler(answer_id, None, None).del_answer_record_in_tbl()
    pass


class answer_handler(object):
    def __init__(self,
                 answer_id,
                 answer_info,
                 user_id):
        self.answer_id = answer_id
        self.answer_info = answer_info
        self.user_id = user_id
        self.db = current.db
    def update_to_answer_tbl(self):
        db = current.db
        try:
            row = db(db.answer_tbl.id == self.answer_id).select().first()
            row.update_record(answer_info = self.answer_info)
        except:
            log.error('cant update answer')
        pass

    def add_to_answer_tbl(self, question_id):
        db = current.db
        answer_id = None
        try:
            answer_id = db.answer_tbl.insert(answer_info = self.answer_info,
                                         question_id = question_id,
                                         author_info = self.user_id)
        except:
            log.error("cant create answer record")
        return answer_id

    def del_answer_record_in_tbl(self):
        db = current.db
        db(db.answer_tbl.id == self.answer_id).delete()
        pass
