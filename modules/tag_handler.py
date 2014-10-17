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
    rst = question_tag_handler()._handle_new_tag_from_user(tag_info)
    return rst

def save_tag_info_for_user(tag_list, auth):
    """
    save tag info in to tag user tbl
    """
    rst = user_tag_handler(auth).update_new_tag_list(tag_list)
    return rst



class user_tag_handler(object):
    def __init__(self, auth):
        self.db = current.db
        self.auth = auth
    def verify_tag(self, tag_info):
        tag_id = tag_tbl_handler().get_id_by_name(tag_info)
        if not tag_id:
            tag_id = tag_tbl_handler().create_new_tag(tag_info)
        return tag_id

    def create_tag(self, tag_info):
        db = self.db
        tag_id = self.verify_tag(tag_info)
        id = db.user_tag_tbl.insert(user_info = self.auth.user.id,
                                    tag_info = tag_id)
        return True

    def create_tag_list(self, tag_list):
        db = self.db
        for tag in tag_list:
            tag_id = self.verify_tag(tag)
            id = db.user_tag_tbl.insert(user_info = self.auth.user.id,
                                        tag_info = tag_id)
            if not id:
                return False
        return True
    def update_new_tag_list(self, tag_data):
        db = self.db
        db(db.user_tag_tbl.user_info == self.auth.user.id).delete()
        if type(tag_data) == list:
            rst = self.create_tag_list(tag_data)
        else:
            rst = self.create_tag(tag_data)
        if not rst:
            return False
        return True
    def get_tag_info(self):
        db = self.db
        tag_info = db(db.user_tag_tbl).select()
        tag_list = []
        for tag in tag_info:
            tag_data = db(db.tag_tbl.id == tag.tag_info).select()[0]
            tag_list.append(tag_data.name)
        return tag_list








class tag_tbl_handler(object):
    def __init__(self):
        self.db = current.db
    def create_new_tag(self, tag_info):
        db = self.db
        try:
            record_id = db.tag_tbl.insert(name = tag_info)
            return record_id
        except:
            log.error(" cant insert to db")
            return None

    def get_id_by_name(self, tag_name):
        #search for tag_name in db
        db = self.db
        tag_rslt = db(db.tag_tbl.name == tag_name).select().first()
        if not tag_rslt:
            return False
        else:
            return tag_rslt.id

    def get_id_by_name_if_not_exist_update_new(self, tag_name):
        tag_id = self.get_id_by_name(tag_name)
        if tag_id:
            return tag_id
        else:
            try:
                tag_id =  self.create_new_tag(tag_name)
                return tag_id
            except:
                log.error('cant update tag tbl')
                return False
        return False

    def get_id_list_from_tag_name_list(self, tag_info):
        id_list = []
        if type(tag_info) == list:
            for tag in tag_info:
                id_list.append(self.get_id_by_name(tag))
        else:
            id_list.append(self.get_id_by_name(tag_info))

        return id_list

    def get_id_list_from_tag_name_list_update_if_necessary(self, tag_info):
        id_list = []
        if type(tag_info) == list:
            for tag in tag_info:
                id_list.append(self.get_id_by_name_if_not_exist_update_new(tag))
        else:
            id_list.append(self.get_id_by_name_if_not_exist_update_new(tag_info))

        return id_list

    def get_all_tag_info_from_db(self):
        db = self.db
        tag_list = []
        tag_record_list = db(db.tag_tbl).select()
        for tag in tag_record_list:
            tag_list.append(tag.name)


        return tag_list

    def get_name_list_from_record_list(self, record):
        tag_name_list = []
        for data in record:
            tag_info = db(db.tag_tbl.id == data.tag_info).select()[0]
            tag_name_list.append(tag_info.name)
        return tag_name_list



class question_tag_handler(object):
    def __init__(self):
        self.db = current.db


    def add_tag_for_question(self,question_id, tag_list):
        db = self.db

        tag_id_list = tag_tbl_handler().get_id_list_from_tag_name_list_update_if_necessary(tag_list)
        for tag_id in tag_id_list:
            try:
                id = db.question_tag_tbl.insert(question_info = question_id,
                                                tag_info = tag_id)
            except:
                log.error("db false")
                return False

        return True

    def search_for_related_tag_in_tbl(self, tag_info):
        """
        search for all tag in db
        find tag start with tag_info
        """
        tag_list =''
        tag_info = tag_info.strip().lstrip()
        db = self.db
        all_tag_list = tag_tbl_handler().get_all_tag_info_from_db()

        if len(all_tag_list):
            tag_list_start_with = [m for m in all_tag_list if m.startswith(tag_info.capitalize())]
            tag_list_include = [m for m in all_tag_list if (tag_info in m)]
            tag_list = list(set(tag_list_start_with + tag_list_include))
        else:
            return False
        return tag_list

    def get_tag_id_list_of_a_question(self, question_id):
        db = self.db
        tag_list = db(db.question_tag_tbl.question_info == question_id).select()
        tag_id_list = []
        for tag_record in tag_list:
            tag_id_list.append(tag_record.tag_info)
        return tag_id_list


    def get_tag_name_list_of_a_question(self, question_id):
        db = self.db
        tag_list = db(db.question_tag_tbl.question_info == question_id).select()
        tag_name_list = []
        for tag_record in tag_list:
            try:
                tag_name = db(db.tag_tbl.id == tag_record.tag_info).select()[0]
            except:
                log.error('no record in tag_tbl...mustbe error')
            tag_name_list.append(tag_name.name)
        return tag_name_list



    def delete_question_tag(self, question_id):
        db = self.db
        try:
            db(db.question_tag_tbl.question_info == question_id).delete()
            db.commit()
            return True
        except:
            log.error("db error")
        return False

    def update_new_tag_list_to_db(self, question_id, new_tag_list):
        """
            select tag_list to delete
            update new tag_list to db
        """
        db = self.db
        try:
            self.delete_question_tag(question_id)
            if new_tag_list:
                self.add_tag_for_question(question_id, new_tag_list)
            return True
        except:
            log.error("fail update tag")
            return False







