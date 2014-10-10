__author__ = 'huyheo'
"""
Syntax:
 python web2py.py -S chuotnhat -M -R applications/chuotnhat/unittest/test_tag_handler.py
"""
import unittest
import gluon
from gluon.globals import Request

import os
file_path = os.path.join(os.getcwd(),'applications','chuotnhat')
execfile(os.path.join(file_path,'models','db.py'), globals())
execfile(os.path.join(file_path,'controllers','default.py'), globals())

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
    user_id =  db.auth_user.insert(first_name = 'lala')
    user_record = db(db.auth_user.id == user_id).select()[0]
    auth.user = user_record
