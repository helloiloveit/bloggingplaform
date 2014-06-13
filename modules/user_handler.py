__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *
from tag_handler import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)


def update_self_introduction(request, auth):
    introduction_info = request.vars.self_introduction
    user_id = auth.user.id
    user_profile_id = user_profile_handler().update_self_introduction(introduction_info, auth.user.id)
    return user_profile_id



class user_profile_handler(object):
    def __init__(self):
        self.db = current.db

    def update_self_introduction(self, introduction_info, user_id):
        db = self.db
        try:
            row = db(db.user_profile.user_info == user_id).select().first()
            if not row:
                profile_id = db.user_profile.insert(user_info = user_id,
                                                self_introduction = introduction_info)
                return profile_id
            else:
                row.update_record(question_info = question_info,
                              question_detail_info = question_detail_info)
                return row.id
        except:
            log.error(" error updating db")
            return False

