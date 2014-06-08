__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)



def handle_tag_in_tag_tbl(tag_info):
    """
    search for tag in database. update new tag if necessary
    if tag is found , return tag value
    """
    tag_info = tag_info.capitalize()
    rst = question_tag_handler().handle_new_tag_from_user(tag_info)
    return rst

class question_tag_handler(object):
    def __init__(self):
        self.db = current.db

    def check_if_tag_is_in_tbl(self, tag_name):
        #search for tag_name in db
        db = self.db
        tag_id = db(db.tag_tbl.name == tag_name).select()
        if not len(tag_id):
            return False
        else:
            return True
    def insert_tag_to_tbl(self, tag_name):
        #search for tag_name in db
        db = self.db
        try:
            record_id = db.tag_tbl.insert(name = tag_name)
            return record_id
        except:
            log.error(" cant insert to db")
            return None

    def handle_new_tag_from_user(self, tag_name):
        if self.check_if_tag_is_in_tbl(tag_name):
            return True
        else:
            if not self.insert_tag_to_tbl(tag_name):
                return None
            else:
                return True

    def search_for_related_tag_in_tbl(self):
        db = self.db
        tag_list = db(db.tag_tbl).select()
        return tag_list





