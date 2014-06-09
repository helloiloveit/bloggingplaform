__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *
from tag_handler import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)


def post_new_question(request, auth, session):
    question_txt = request.vars.question_info
    question_detail_txt = request.vars.question_detail_info
    user_id = auth.user.id
    question_id = question_handler().create_new_record_in_question_tbl(question_txt,
                                                                question_detail_txt,
                                                                user_id,
                                                            session.tag_list_store)
    return question_id
def delete_a_question(request):
    question_id = request.args[0]
    question_handler().delete_question_in_db(question_id)
    return

def update_a_question(request, tag_list):
    question_id = request.args[0]
    question_handler().update_to_question_tbl(question_id, request.vars.question_info, request.vars.question_detail_info, tag_list)
    return





def user_like_a_question(request, auth):
    question_id = request.vars.question_id
    record_id = question_handler().vote_up_a_question(question_id, auth.user.id)
    return record_id

def user_unlike_a_question(request, auth):
    question_id = request.vars.question_id
    result = question_handler().vote_down_a_question(question_id, auth.user.id)
    return result

class question_handler(object):
    def __init__(self):
        self.db = current.db

    def create_new_record_in_question_tbl(self,question_info, question_detail_info, user_id, tag_list):
        """
            create new question record
            create new tag for this question
        """

        db = self.db
        question_id = None
        try:
            question_id = db.question_tbl.insert( question_info = question_info,
                                                question_detail_info = question_detail_info,
                                                writer = user_id)
            log.info(" successful create a tbl")
        except:
            log.error(' cant create tbl')
        log.info("question_id = %s",question_id)

        #tag list
        rst = self.add_tag_for_question(question_id, tag_list)
        if not rst:
            return False

        return question_id

    def add_tag_for_question(self,question_id, tag_list):
        db = self.db
        tag_id_list = question_tag_handler().handle_new_tag_list_from_user(tag_list)
        import pdb;pdb.set_trace()
        for tag_id in tag_id_list:
            try:
                id = db.question_tag_tbl.insert(question_info = question_id,
                                                tag_info = tag_id)
            except:
                log.error("db false")
                return False

        return True


    def update_to_question_tbl(self, question_id, question_info, question_detail_info, tag_list):
        db = self.db
        try:
            row = db(db.question_tbl.id == question_id).select().first()
            row.update_record(question_info = question_info,
                          question_detail_info = question_detail_info)
            #update tag
            #later
        except:
            log.error('cant update tbl')
        pass

    def delete_question_in_db(self, question_id):
        if self.delete_record_in_question_tbl(question_id):
            #delete question id in tag
            if question_tag_handler().delete_question(question_id):
                return True
        return False

    def delete_record_in_question_tbl(self, question_id):
        db = self.db
        try:
            db(db.question_tbl.id == question_id).delete()
            return True
        except:
            return False
        pass

    def vote_up_a_question(self, question_id, audience_id):
        db = self.db
        question_like_id =None
        try:
            question_like_id = db.question_like_tbl.insert( question_id = question_id,
                                                            user_info = audience_id)
        except:
            log.error('cant create tbl')
        return question_like_id

    def vote_down_a_question(self, question_id, audience_id):
        db = self.db
        try:
            #check if user did like this question or not
            # if yes . delete this record
            # if no   return flag  0: success 1: db failed 2: user already not like it
            like_record = db((db.question_like_tbl.question_id == question_id)&(db.question_like_tbl.user_info == audience_id )).select()
            if len(like_record):
                db(db.question_like_tbl.id == like_record[0].id).delete()
                return SUCCESS_RESULT
            else:
                return DB_IS_UPDATED_ALREADY

        except:
            log.error('cant update db')
            return DB_FAILED
        return DB_FAILED

    def report_a_question(self, question_id, audience):
        db  = self.db
        question_report_id =None
        try:
            question_report_id = db.question_report_tbl.insert(question_id = question_id,
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
