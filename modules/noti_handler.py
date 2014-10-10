__author__ = 'huyheo'


import logging
from gluon import *

from ConstantDefinition import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)





class noti_handler(object):
    def __init__(self, question_id):
        self.question_id = question_id
        # add to task queue

    def add_to_gae_task_queue(self):
        from google.appengine.api import taskqueue
        taskqueue.add(url='/add_gae_queue', params={'question_id': self.question_id})

    def create_href(self):
        return "huyheo"

    def create_message(self):
        return "this is test message"

    def send_fb_noti(self, user_id, href_link, noti_mess):
        from gluon.tools import fetch
        url_2 = "https://graph.facebook.com/"+ user_id + "/notifications"
        values =   { 'access_token': APP_ACCESS_TOKEN, 'href':href_link, 'template':noti_mess}
        rsp = fetch(url_2, values)
        return rsp