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


class tag_tbl_handler(object):
    def __init__(self):
        self.db = current.db
    def create_new_tag(self, tag_info):
        db = self.db
        record_id = db.tag_tbl.insert( name = tag_info)
        if record_id:
            return True




class question_tag_handler(object):
    def __init__(self):
        self.db = current.db

    def add_tag_for_question(self,question_id, tag_list):
        db = self.db

        tag_id_list = question_tag_handler()._handle_new_tag_data_from_user(tag_list)
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
        db = self.db
        all_tag_list = self. _get_all_tag_info_from_db()
        if len(all_tag_list):
            tag_list = [m for m in all_tag_list if m.startswith(tag_info)]
        else:
            return False
        return tag_list


    def _check_if_tag_is_in_tbl(self, tag_name):
        #search for tag_name in db
        db = self.db
        tag_rslt = db(db.tag_tbl.name == tag_name).select().first()
        if not tag_rslt:
            return False
        else:
            return tag_rslt.id
    def _insert_tag_to_tbl(self, tag_name):
        #search for tag_name in db
        db = self.db
        try:
            record_id = db.tag_tbl.insert(name = tag_name)
            return record_id
        except:
            log.error(" cant insert to db")
            return None

    def _handle_new_tag_from_user(self, tag_name):
        tag_id = self._check_if_tag_is_in_tbl(tag_name)
        if tag_id:
            return tag_id
        else:
            try:
                tag_id =  self._insert_tag_to_tbl(tag_name)
                return tag_id
            except:
                log.error('cant update tag tbl')
                return False

        return False

    def _handle_new_tag_data_from_user(self, tag_info):
        id_list = []
        import pdb; pdb.set_trace()
        if type(tag_info) == list:
            for tag in tag_info:
                id_list.append(self._handle_new_tag_from_user(tag))
        else:
            id_list.append(self._handle_new_tag_from_user(tag_info))

        return id_list


    def _get_all_tag_info_from_db(self):
        db = self.db
        tag_list = []
        tag_record_list = db(db.tag_tbl).select()
        for tag in tag_record_list:
            tag_list.append(tag.name)


        return tag_list

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
            self.add_tag_for_question(question_id, new_tag_list)
            return True
        except:
            log.error("fail update tag")
            return False







