__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *
from tag_handler import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)


def handler_fb_noti(request):
    """
        call fb_noti_handler indirectly to make test easier
    """
    question_id = request.vars['question_id']
    noti_data = noti_handler(question_id)
    user_info_list = noti_data.get_targeted_user()
    db = current.db
    for temp in user_info_list:
        user_record = db(db.auth_user.id == temp).select()[0]
        # get user list to send noti
        href_link = noti_handler(question_id).create_href()
        fb_noti_handler(user_record.username, href_link, noti_data.create_message()).send()


class fb_noti_handler(object):
    def __init__(self, user_id, href_link, noti_mess):
        self.user_id = user_id
        self.href_link = href_link
        self.noti_mess = noti_mess

    def send(self):
        from gluon.tools import fetch
        url_2 = "https://graph.facebook.com/"+ self.user_id + "/notifications"
        values =   { 'access_token': APP_ACCESS_TOKEN, 'href':self.href_link, 'template':self.noti_mess}
        rsp = fetch(url_2, values)
        return rsp

    def __call__(self, *args, **kwargs):
        print 'call fb noti'



class noti_handler(object):
    def __init__(self, question_id):
        self.question_id = question_id
        self.db = current.db
        # add to task queue

    def add_to_gae_task_queue(self, request):
        """
        add request parameter for the ease of testing without gae
        """
        try:
            from google.appengine.api import taskqueue
            taskqueue.add(url='/add_gae_queue', params={'question_id': self.question_id})
        except:
            request.vars.update({'question_id': self.question_id})
            handler_fb_noti(request)


    def create_href(self):
        log.info("")
        return "fb_question" + "?id=" + str(self.question_id)

    def create_message(self):
        db = self.db
        question_record = db(db.question_tbl.id == self.question_id).select().first()
        return question_record.question_info


    def get_targeted_user(self):
        """
        get tag list of question
        query user of tag
        """
        db = self.db
        tag_id_list = question_tag_handler().get_tag_id_list_of_a_question(self.question_id)
        user_list = []
        for tag_id in tag_id_list:
            user_data = db(db.user_tag_tbl.tag_info == tag_id).select()
            if len(user_data):
                for data in user_data:
                    if data.user_info not in user_list:
                        user_list.append(data.user_info)
        return user_list

    def send_noti_to_user(self):
        user_list = self.get_targeted_user()
        for user_id in user_list:
            fb_noti_handler(user_id, "huyheo", "test notification").send()
            #noti_handler(question_id).send_fb_noti(user_id, "huyheo", " test notification ")

