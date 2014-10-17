# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import json
import logging
from database_handler import *
from tag_handler import *
from noti_handler import *
from user_handler import *
from text_handler import *
import xml.etree.ElementTree as ET

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)

from ConstantDefinition import *
try:
    import json
except ImportError:
    from gluon.contrib import simplejson as json
from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount

#global variable for page number
#end global var
def term_of_use():
    return dict()

def search_box():
    return dict()
def test_tinyMCE():
    return dict()

def test_facebook():
    return dict()

def create_new_tag():
    if not request.vars.tag_info: return ''
    tag_info = request.vars.tag_info.capitalize()
    rst = tag_tbl_handler().create_new_tag(tag_info)
    if rst:
        return True

    else:
        return False

def tag_handler():
    if not request.vars.tag_info: return ''
    tag_info = request.vars.tag_info
    selected = question_tag_handler().search_for_related_tag_in_tbl(tag_info)
    #selected =['tag1','tag2', 'tag3','tag4']
    #selected = [m for m in tag_list if m.name.startswith(tag_info)]
    log.info('selected = %s', selected)
    div_id = "suggestion_box"

    if not selected:
        temp = [DIV('tạo tag moi',
                    _onclick="user_post_new_tag('%s','%s');" %(tag_info, div_id),
                    _onmouseover="this.style.backgroundColor='yellow'",
                    _onmouseout="this.style.backgroundColor='white'"
        )]
    else:
        temp = [DIV(k,
                    _onclick="user_select_tag_handler('%s','%s');" %(k,div_id),
                    _onmouseover="this.style.backgroundColor='yellow'",
                    _onmouseout="this.style.backgroundColor='white'"
        ) for k in selected]


    return DIV(
                temp, _id ="%s" % div_id
                )



def user():
    """
    if request.env.REQUEST_METHOD =='POST':
        #save self introduction to db
        update_self_introduction(request, auth)
        redirect(URL(r = request, f= 'user', args = 'profile'))
    if request.env.REQUEST_METHOD =='GET':
        if request.args[0] == 'login':
            return dict(form = auth())
        profile_info = db(db.user_profile.user_info == auth.user.id).select().first()
        return dict(user_profile = profile_infoimport pdb; pdb.set_trace())
    """
    return dict(form = auth())

def user_profile():
    response.title ='user_profile'
    follow_flag = False
    view_my_profile= False
    if request.env.REQUEST_METHOD =='GET':
        target_person_id = request.vars.user_id
        user_info = db(db.auth_user.id == target_person_id).select().first()
        profile_info = db(db.user_profile.user_info == target_person_id).select().first()
        if not profile_info:
            profile_id = create_basis_user_profile(target_person_id)
            if profile_id:
                profile_info = db(db.user_profile.id == profile_id).select().first()
        #check if user view its own profile
        if auth.is_logged_in():
            if target_person_id == str(auth.user.id):
                # view my profile
                view_my_profile = True
        try:
            #if user is logged in
            follow_record = db((db.follow_info_tbl.followed_user == target_person_id)&(db.follow_info_tbl.following_user == auth.user.id )).select().first()
        except:
            # not login
            follow_record = False
            pass
        if follow_record:
            follow_flag = True
        else:
            follow_flag = False
        #following
        following_list = db(db.follow_info_tbl.followed_user == target_person_id).select()
        #followed
        followed_list = db(db.follow_info_tbl.following_user == target_person_id).select()
        response.title = user_info.first_name
        #answer list
        answer_list = db(db.answer_tbl.author_info == user_info.id).select()
        answer_list, page_num, view_more_flag = _handle_page_num(request, answer_list)

        return dict(person_profile = profile_info,
                    person_info= user_info,
                    follow_flag = follow_flag,
                    view_my_profile=view_my_profile,
                    following_list = following_list,
                    followed_list = followed_list,
                    answer_list = answer_list,
                    page_num = page_num,
                    view_more_flag = view_more_flag)
    return dict()

def edit_user_profile():
    if request.env.REQUEST_METHOD =='POST':
        rst = update_self_introduction(request, auth)
        redirect(URL('user_profile', vars=dict(user_id=request.vars.user_id)))
        return dict()
    elif request.env.REQUEST_METHOD =='GET':
        target_person_id = request.vars.user_id
        profile_info = db(db.user_profile.user_info == target_person_id).select().first()
        user_info = db(db.auth_user.id == target_person_id).select().first()
        try:
            #if user is logged in
            follow_record = db((db.follow_info_tbl.followed_user == target_person_id)&(db.follow_info_tbl.following_user == auth.user.id )).select().first()
        except:
            # not login
            follow_record = False
            pass
        if follow_record:
            follow_flag = True
        else:
            follow_flag = False
        #following
        following_list = db(db.follow_info_tbl.followed_user == target_person_id).select()
        #followed
        followed_list = db(db.follow_info_tbl.following_user == target_person_id).select()
        return dict(person_profile = profile_info,
                    person_info= user_info,
                    follow_flag = follow_flag,
                    following_list = followed_list,
                    followed_list = followed_list)

    return dict()

def update_profile():
    rst = update_self_introduction(request, auth)
    if rst:
        return True
    else:
        return False
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    log.info('index')
    redirect(URL(f= 'question_list'))
    return dict()

def fb_noti():
    data = {
    "access_token": session.token['access_token'],
    "href": "www.chuotnhat.vn",
    "template":"you have to be in the game"
    }
    import urllib
    import urllib2
    import pdb; pdb.set_trace()
    data = urllib.urlencode(data)
    url = 'http://www.facebook.com/' + str(auth.user.username) +  '/notifications'
    html = urllib2.urlopen(url)
    print html
    """
    from gluon.tools import fetch
    page = fetch('http://www.facebook.com/' + str(auth.user.username) +  '/notifications', data)
    log.info(page);
    """

def set_meta_data(question):
    """
    response.meta.keywords
    response.meta.description
    response.meta.generator
    response.meta.author
    """
    response.meta.author =''
    input_str = question.question_detail_info
    input_str = input_str.decode('utf-8')
    temp = html_to_text(input_str)
    response.meta.description =temp.encode('utf8')
    response.title = question.question_info
    return

def question():
    """
    Display blog by id
    """

    if request.env.REQUEST_METHOD == 'POST':
        create_new_answer(request, auth)
        redirect(URL(r = request, f= 'question', args = request.vars.question_id))
    elif request.env.REQUEST_METHOD == 'GET':
        question = None
        answer_list = []
        user_id =''
        try:
            question = db(db.question_tbl.id == int(request.args[0])).select()[0]
            user_info = db(db.auth_user.id == question.writer).select().first()
            try:
                answer_list = db(db.answer_tbl.question_id == question.id).select()
            except:
                log.error('cant query answer db')
        except:
            log.error('cant query a question from db')
            question = None
        #like list
        like_list = db(db.question_like_tbl.question_id==question.id).select()
        #related question list
        related_question_list = db(db.question_tbl).select()
        #set meta
        set_meta_data(question)
        return dict(item = question,
                    like_list = like_list,
                    comment_list = answer_list,
                    user_info = user_info,
                    related_question_list = related_question_list)

@auth.requires_login()
def edit_question():
    """
    Edit blog
    """
    log.info("edit question")
    if request.env.REQUEST_METHOD == 'GET':
        question = db(db.question_tbl.id == request.args[0]).select()[0]
        tag_list = question_tag_handler().get_tag_name_list_of_a_question(request.args[0])
        return dict(question = question , tag_list = tag_list)
    elif request.env.REQUEST_METHOD == 'POST':
        update_a_question(request)
        redirect(URL(r = request, f= 'question', args = [request.args[0]]))

    return dict()

@auth.requires_login()
def delete_question():
    selection = request.vars
    if request.env.REQUEST_METHOD == 'GET':
        return dict()
    elif request.env.REQUEST_METHOD == 'POST':
        if selection['selection'] == "YES":
            delete_a_question(request)
            redirect(URL(r = request, f= 'question_list'))
        elif selection['selection'] == "NO":
            redirect(URL(r = request, f= 'question', args = [request.args[0]]))
    return dict()

@auth.requires_login()
def edit_answer():
    """
    edit answer
    """
    if request.env.REQUEST_METHOD == 'GET':
        answer_id = request.args[0]
        origin_url = request.vars.origin
        session.EDIT_ANSWER_ORIGIN_URL = origin_url
        answer = db(db.answer_tbl.id == answer_id).select().first()
        return dict(answer = answer)
    elif request.env.REQUEST_METHOD == 'POST':
        update_an_answer(request)
        answer_id = request.vars.answer_id
        answer = db(db.answer_tbl.id == answer_id).select().first()
        question_id = answer.question_id
        if session.EDIT_ANSWER_ORIGIN_URL == 'user_profile':
            redirect(URL(r = request, f= 'user_profile', vars = {'user_id':auth.user.id}))
        elif session.EDIT_ANSWER_ORIGIN_URL == 'question':
            redirect(URL(r = request, f= 'question', args = [question_id]))

    return dict()

@auth.requires_login()
def delete_answer():
    selection = request.vars
    if request.env.REQUEST_METHOD == 'GET':
        answer_id = request.args[0]
        return dict(answer_id = answer_id)
    elif request.env.REQUEST_METHOD == 'POST':
        answer_id = selection['answer_id']
        answer = db(db.answer_tbl.id == answer_id).select().first()
        question_id = answer.question_id
        if selection['selection'] == "YES":
            delete_a_answer(request)
        elif selection['selection'] == "NO":
            pass
        redirect(URL(r = request, f= 'question', args = [question_id]))
    return dict()

    return dict()

def create_data_for_question_list_for_test():
    import pdb; pdb.set_trace()
    user_record = db(db.auth_user).select().first()
    if not user_record:
        user_id =  db.auth_user.insert(first_name = 'first_user', email = 'first_user_email@gmail.com')
    else:
        user_id = user_record.id
    auth.user = db(db.auth_user.id == user_id).select()[0]
    for i in range(1,10,1):
        question = "Lam sao de giai quyet duoc van de nay h troi oi " + str(i)
        question_detail_info = """
        Đối với một lập trình viên trong thế giới công nghệ, có một thứ mà có thể kéo chúng ta ra khỏi nhà và đến nơi làm việc, đó là niềm vui và đam mê trong việc lập trình. Nhưng để khiến cho công việc thực sự vui vẻ và có thể tạo ra một niềm hứng khởi vĩnh cửu, chúng ta cần phải biết những điều căn bản để giúp trở thành một nhà lập trình viên giỏi. - See more at: http://toancauxanh.vn/news/technology/10-cach-hay-de-tro-thanh-mot-lap-trinh-vien-gioi#sthash.ZZ4aV4xY.dpufb
         """+ str(i)
        tag_list = ["tag1","tag2","tag3"]
        question_id = question_handler().create_new_record_in_question_tbl(question, question_detail_info, user_id, tag_list)

def _handle_page_num(request, items):
    view_more_flag= False
    page_num_request = request.vars.page_num
    page_num = 0
    if page_num_request == None:
        page_num = 0
    else:
        page_num = page_num_request
    try:
        if len(items):
            display_list = items[int(page_num)*12:int(page_num)*12+12]
        else:
            display_list =[]
        if len(items) > (int(page_num)*12 + 12):
            view_more_flag = True

    except:
        log.error('cant query data from db')
        display_list = []
    return display_list, page_num, view_more_flag

def question_list():
    """
    test data
    """
    log.info('question list')
    log.info(request.env.REQUEST_METHOD)
    response.title = 'Chuot Nhat'
    items = db(db.question_tbl).select()
    display_list, page_num, view_more_flag= _handle_page_num(request, items)

    return dict(items= display_list, page_num = page_num, view_more_flag=view_more_flag)

def get_header(text):
    """
        get header of article
    """
    header_position =text.find("<p>&nbsp;</p>")
    log.info("header_position = %d", header_position)
    header_text =  request.vars.editor1[:header_position]
    return header_text


def mission_info():
    return dict()


@auth.requires_login()
def post():
    log.info("request.vars = %s",request.vars)
    return dict(article_tag_list ="" )




@auth.requires_login()
def post_question():
    question_id = post_new_question(request, auth)
    if question_id:
        #add to queue
        noti_handler(question_id).add_to_gae_task_queue(request)
        redirect(URL(r = request, f= 'question', args = question_id))
    return dict()



####### answer ######
@auth.requires_login()
def like_an_answer():
    rst= user_like_an_answer(request, auth)
    like_record = db((db.answer_like_tbl.answer_id == request.vars.answer_id)).select()
    return len(like_record)

def unlike_an_answer():
    rst = user_unlike_an_answer(request, auth)
    like_record = db((db.answer_like_tbl.answer_id == request.vars.answer_id)).select()
    return len(like_record)

@auth.requires_login()
def user_update_an_answer():
    update_an_answer(request)
    return dict()
@auth.requires_login()
def user_del_an_answer():
    del_an_answer(request)
    return dict()


##############################
@auth.requires_login()
def like_a_question():
    count_like = user_like_a_question(request, auth)
    return count_like

@auth.requires_login()
def unlike_a_question():
    count_like = user_unlike_a_question(request, auth)
    return count_like

def report_a_question():
    #user_report_a_question(request, auth)
    return "reported"

##############follow##########
@auth.requires_login()
def follow_a_person():
    rst = user_follow_a_person(request, auth)
    if rst:
        return "followed"
    else:
        return "error"
def unfollow_a_person():
    rst = user_unfollow_a_person(request, auth)
    if rst :
        return "follow"
    else:
        return "error"




############################################
################facebook####################
############################################

def fb_main():
    """
    test data
    """
    tag_info = []
    if auth.is_logged_in():
        try:
            tag_info = user_tag_handler(auth).get_tag_info()
        except:
            pass
    return dict(tag_list = tag_info)

def fb_save_tag_list():
    tag_list = request.vars['tag_info[]']
    rst = save_tag_info_for_user(tag_list, auth)
    # save tag list to db for generating question
    if not rst:
        return 0
    return 1

def add_gae_queue():
    handler_fb_noti(request)

def fb_test():
    log.info('lalal')
    send_fb_noti("540428388", " test notification ")
    return dict()

def fb_test_queue():
    from google.appengine.api import taskqueue
    log.info('lalal')
    taskqueue.add(url='/add_gae_queue', params={'question_id': '123'})
    return dict()

@auth.requires_login()
def fb_post():
    log.info("request.vars = %s",request.vars)
    return dict(article_tag_list ="" )
