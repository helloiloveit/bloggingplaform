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
from user_handler import *

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)

from ConstantDefinition import *
try:
    import json
except ImportError:
    from gluon.contrib import simplejson as json
from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount



def test_jquery():
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
    tag_info = request.vars.tag_info.capitalize()
    selected = question_tag_handler().search_for_related_tag_in_tbl(tag_info)
    #selected =['tag1','tag2', 'tag3','tag4']
    #selected = [m for m in tag_list if m.name.startswith(tag_info)]
    div_id = "suggestion_box"

    if not len(selected):
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
        return dict(user_profile = profile_info)
    """
    return dict(form = auth())

def user_profile():
    if request.env.REQUEST_METHOD =='GET':
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
    print T.current_languages
    """
    T.force('fr')
    T.set_current_languages('en', 'fr')
    print T.current_languages
    """
    redirect(URL(r = request, f= 'question_list', args = ''))
    return dict()


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
        import pdb; pdb.set_trace()
        update_a_question(request)
        redirect(URL(r = request, f= 'question', args = [request.args[0]]))

    return dict()

@auth.requires_login()
def delete_question():
    selection = request.vars
    if selection['selection'] == "YES":
        delete_a_question(request)
        redirect(URL(r = request, f= 'question_list'))
    elif selection['selection'] == "NO":
        redirect(URL(r = request, f= 'question', args = [request.args[0]]))
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

def question_list():
    """
    test data
    """
    record = db(db.auth_user).select()

    question_list = db(db.question_tbl).select()
    if not len(question_list):
        pass
        #create_data_for_question_list_for_test()
    """
    end test data
    """
    items= []


    try:
        items = db(db.question_tbl).select()

    except:
        log.error('cant query data from db')
    return dict(items= items)

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
    tag_info = request.vars.tag_list
    tag_list = tag_info.split(',')
    question_id = post_new_question(request, auth, tag_list)
    if question_id:
        redirect(URL(r = request, f= 'question', args = question_id))
    return dict()


@auth.requires_login()
def user_modify_question():
    update_a_question(request, session.tag_list_store)
    return dict()


####### answer ######
@auth.requires_login()
def like_an_answer():
    user_like_an_answer(request, auth)
    return 'unlike'

def unlike_an_answer():
    user_unlike_an_answer(request, auth)
    return True

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
    user_like_a_question(request, auth)
    return "unlike"

@auth.requires_login()
def unlike_a_question():
    user_unlike_a_question(request, auth)
    return "like"

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


#those code is for manage meta data not using right now
# using flickr for photo uploading
@auth.requires_login()
def show_image():

    image_data = db(db.pic_store).select()
    #image = image_data.pic

    form = SQLFORM(db.pic_store)
    if form.process().accepted:
        response.flash = 'movie info is posted'
    return dict(form = form)
@auth.requires_login()
def manage_image():
    grid = SQLFORM.smartgrid(db.pic_store)
    return dict(grid=grid)

@auth.requires_login()
def manage_article_tag():
    grid = SQLFORM.smartgrid(db.article_tag)
    return dict(grid=grid)