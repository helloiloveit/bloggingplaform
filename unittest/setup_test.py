__author__ = 'huyheo'
"""
Syntax:
 python web2py.py -S chuotnhat -M -R applications/chuotnhat/unittest/test_user_tag_handler.py
"""
import unittest
import gluon
from gluon.globals import Request

import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat')
execfile(os.path.join(file_path,'models','db.py'), globals())
execfile(os.path.join(file_path,'controllers','default.py'), globals())

user_record_1 = ''
user_record_2 = ''
user_record_3 = ''

def set_up_basic_environment():
    #set up request
    env = dict()
    request = Request(env)
    #clear all table
    db.auth_user.truncate()
    db.question_tbl.truncate()
    db.tag_tbl.truncate()
    db.user_tag_tbl.truncate()
    db.question_tag_tbl.truncate()
    db.commit()

    #set up user
    global user_record_3, user_record_2, user_record_1
    user_id_1 =  db.auth_user.insert(first_name = 'lala', username ='540428388')
    user_id_2 =  db.auth_user.insert(first_name = 'lala', username ='100005290308589')
    user_id_3 =  db.auth_user.insert(first_name = 'lala', username ='100005841888554')
    user_record_3 = db(db.auth_user.id == user_id_3).select()[0]
    user_record_2 = db(db.auth_user.id == user_id_2).select()[0]
    user_record_1 = db(db.auth_user.id == user_id_1).select()[0]
    auth.user = user_record_1

class AnswerHandlingUility(object):
    def __init__(self, question_id):
        self.question_id = question_id
    def create_answer(self, answer_info, user_id):
        answer_id = answer_handler().create_new_answer(self.question_id, answer_info, user_id)
        return answer_id


class QuestionHandlingUtility(object):
    def __init__(self, question, question_detail_info, tag_list):
        self.question = question
        self.question_detail_info = question_detail_info
        self.tag_info = tag_list



    def add_value_of_question_to_request(self, question_id):
        request.vars.question_info = self.question
        request.vars.question_detail_info = self.question_detail_info
        if question_id:
            #question is existed
            request.vars.question_id = question_id
        request.vars.tag_list = self.tag_info

    def create_a_question(self):
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)
        return question_id

    def create_a_question_skip_add_queue(self):
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)
        if question_id:
            noti_handler(question_id).add_to_gae_task_queue()
        return question_id

    def create_a_question_by_user(self,auth):
        self.add_value_of_question_to_request(None)
        question_id = post_new_question(request, auth)

        return question_id
