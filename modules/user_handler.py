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


def user_follow_a_person(request, auth):
    person_id = request.vars.person_id
    user_id = auth.user.id
    follow_id = follow_feature_handler(user_id).follow(person_id)
    if follow_id:
        return True
    else:
        return False
def user_unfollow_a_person(request, auth):
    person_id = request.vars.person_id
    user_id = auth.user.id
    unfollow_id = follow_feature_handler(user_id).unfollow(person_id)
    if unfollow_id:
        return True
    else:
        return False



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

class follow_feature_handler(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = current.db

    def follow(self, person_id):
        """
        check if person was followed already
        update db
        """
        db = self.db
        follow_record = db((db.follow_info_tbl.followed_user == person_id)&(db.follow_info_tbl.following_user == self.user_id )).select().first()
        if not follow_record:
            id = db.follow_info_tbl.insert(followed_user = person_id,
                                      following_user = self.user_id)
            db.commit()

            return id
        else:
            log.info("already followed")
            return False

    def unfollow(self, person_id):
        """
        check if person was unfollowed already
        update db
        """
        db = self.db
        follow_record = db((db.follow_info_tbl.followed_user == person_id)&(db.follow_info_tbl.following_user == self.user_id )).select().first()
        if follow_record:
            db(db.follow_info_tbl.id == follow_record.id).delete()
            db.commit()
            return True

        else:
            log.info("already unfollowed")
            return False




