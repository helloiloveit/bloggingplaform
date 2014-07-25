__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *
from tag_handler import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)

def get_tag_list(tag_info):
    tag_list = False
    if len(tag_info):
        tag_list = tag_info.split(',')
    else:
        tag_list = False
    return tag_list


def post_new_question(request, auth):
    question_txt = request.vars.question_info
    question_detail_txt = request.vars.editor1
    user_id = auth.user.id
    tag_info = request.vars.tag_list
    tag_list = get_tag_list(tag_info)
    question_id = question_handler().create_new_record_in_question_tbl(question_txt,
                                                                question_detail_txt,
                                                                user_id,
                                                            tag_list)
    return question_id
def delete_a_question(request):
    question_id = request.args[0]
    question_handler().delete_question_in_db(question_id)
    return

def update_a_question(request):
    question_id = request.args[0]
    tag_info = request.vars.tag_list
    tag_list = get_tag_list(tag_info)

    question_handler().update_to_question_tbl(question_id, request.vars.question_info, request.vars.question_detail_info, tag_list)
    return





def user_like_a_question(request, auth):
    question_id = request.vars.question_id
    record_id = question_handler().vote_up_a_question(question_id, auth.user.id)
    db = current.db
    count_like = db((db.question_like_tbl.question_id == question_id)).select()
    return len(count_like)

def user_unlike_a_question(request, auth):
    question_id = request.vars.question_id
    result = question_handler().vote_down_a_question(question_id, auth.user.id)
    db = current.db
    count_like = db((db.question_like_tbl.question_id == question_id)).select()
    return len(count_like)

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
        if tag_list:
            rst = question_tag_handler().add_tag_for_question(question_id, tag_list)
            if not rst:
                log.error('problem create tag infor for question')
                return False
        else:
            log.info('this question doesnt have any tag yet')

        return question_id



    def update_to_question_tbl(self, question_id, question_info, question_detail_info, tag_list):
        db = self.db
        try:
            row = db(db.question_tbl.id == question_id).select().first()
            row.update_record(question_info = question_info,
                          question_detail_info = question_detail_info)
            #update tag
            rst = question_tag_handler().update_new_tag_list_to_db(question_id, tag_list)
            if rst:
                return True
            return False
        except:
            log.error('cant update tbl')
        pass

    def delete_question_in_db(self, question_id):
        if self.delete_record_in_question_tbl(question_id):
            #delete question id in tag
            if question_tag_handler().delete_question_tag(question_id):
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
            #check if user did like this question or not
            like_record = db((db.question_like_tbl.question_id == question_id)&(db.question_like_tbl.user_info == audience_id )).select()
            if len(like_record):
                return SUCCESS_RESULT
            else:
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
    answer_id = answer_handler().add_to_answer_tbl(question_id, answer_info, auth.user.id)
    return answer_id

def update_an_answer(request):
    answer_id = request.vars.answer_id
    answer_info = request.vars.answer_info
    answer_handler().update_to_answer_tbl(answer_id, answer_info)
    pass
def delete_a_answer(request):
    answer_id = request.vars['answer_id']
    answer_handler().del_answer_record_in_tbl(answer_id)
    pass

def user_like_an_answer(request, auth):
    answer_id = request.vars.answer_id
    record_id = answer_handler().vote_up_an_answer(answer_id, auth.user.id)
    return record_id

def user_unlike_an_answer(request, auth):
    answer_id = request.vars.answer_id
    record_id = answer_handler().vote_down_an_answer(answer_id, auth.user.id)
    return record_id

class answer_handler(object):
    def __init__(self):
        self.db = current.db

    def update_to_answer_tbl(self, answer_id, answer_info):
        db = self.db
        try:
            row = db(db.answer_tbl.id == answer_id).select().first()
            row.update_record(answer_info = answer_info)
        except:
            log.error('cant update answer')
        pass

    def add_to_answer_tbl(self, question_id, answer_info, user_id):
        db = self.db
        answer_id = None
        try:
            answer_id = db.answer_tbl.insert(answer_info = answer_info,
                                         question_id = question_id,
                                         author_info = user_id)
        except:
            log.error("cant create answer record")
        return answer_id

    def del_answer_record_in_tbl(self, answer_id):
        db = self.db
        db(db.answer_tbl.id == answer_id).delete()
        pass

    def vote_up_an_answer(self, answer_id, audience_id):
        db = self.db
        answer_like_id =None
        try:
            # check if this user already like it
            like_record = db((db.answer_like_tbl.answer_id == answer_id)&(db.answer_like_tbl.user_info == audience_id )).select()
            if len(like_record):
                return True
            else:
                answer_like_id = db.answer_like_tbl.insert( answer_id = answer_id,
                                                            user_info = audience_id)
        except:
            log.error('cant create tbl')
        return answer_like_id

    def vote_down_an_answer(self, answer_id, audience_id):
        db = self.db
        try:
            #check if user did like this question or not
            # if yes . delete this record
            # if no   return flag  0: success 1: db failed 2: user already not like it
            like_record = db((db.answer_like_tbl.answer_id == answer_id)&(db.answer_like_tbl.user_info == audience_id )).select().first()
            if like_record:
                db(db.answer_like_tbl.id == like_record.id).delete()
                return SUCCESS_RESULT
            else:
                return DB_IS_UPDATED_ALREADY

        except:
            log.error('cant update db')
            return DB_FAILED
        return DB_FAILED

    def report_an_answer(self, answer_id, audience):
        db  = self.db
        answer_report_id =None
        try:
            answer_report_id = db.answer_report_tbl.insert(answer_id = question_id,
                                                               user_info = audience)
        except:
            log.error('cant create tbl')
        return answer_report_id



