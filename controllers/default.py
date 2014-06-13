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

def tag_handler():
    if not request.vars.tag_info: return ''
    tag_list = question_tag_handler().get_all_tag_info_from_db()
    tag_info = request.vars.tag_info.capitalize()
    handle_tag_in_tag_tbl(tag_info)
    selected = [m for m in tag_list if m.startswith(tag_info)]
    return DIV(*[DIV(k,
                     _onclick="jQuery('#month').val('%s')" % k,
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for k in selected])



def user():
    import pdb; pdb.set_trace()
    if request.env.REQUEST_METHOD =='POST':
        #save self introduction to db
        update_self_introduction(request, auth)
        redirect(URL(r = request, f= 'user', args = 'profile'))
    if request.env.REQUEST_METHOD =='GET':
        profile_info = db(db.user_profile.user_info == auth.user.id).select().first()
        return dict(user_profile = profile_info)

    return dict(form = auth())

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #redirect(URL(r = request, f= 'blog', args = 3))
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
        try:
            question = db(db.question_tbl.id == int(request.args[0])).select()[0]
            try:
                answer_list = db(db.answer_tbl.question_id == question.id).select()
            except:
                log.error('cant query answer db')
        except:
            log.error('cant query a question from db')
            question = None
        return dict(item = question, comment_list = answer_list)

#@auth.requires_login()
def edit_question():
    """
    Edit blog
    """
    log.info("edit question")
    import pdb; pdb.set_trace()
    if request.env.REQUEST_METHOD == 'GET':
        question = db(db.question_tbl.id == request.args[0]).select()[0]
        tag_list = question_tag_handler().get_tag_list_of_a_question(request.args[0])
        return dict(question = question , tag_list = tag_list)
    elif request.env.REQUEST_METHOD == 'POST':
        update_a_question(request, session.tag_list_store)
        redirect(URL(r = request, f= 'question', args = [request.args[0]]))

    return dict()

        
def delete_question():
    selection = request.vars
    if selection['selection'] == "YES":
        delete_a_question(request)
        redirect(URL(r = request, f= 'question_list'))
    elif selection['selection'] == "NO":
        redirect(URL(r = request, f= 'question', args = [request.args[0]]))
    return dict()


def create_data_for_question_list_for_test():
    user_id =  db.auth_user.insert(first_name = 'first_user', email = 'first_user_email@gmail.com')
    auth.user = db(db.auth_user.id == user_id).select()[0]
    for i in range(1,10,1):
        question = "this is a new question " + str(i)
        question_detail_info = "detail of question " + str(i)
        tag_list = ["tag1","tag2","tag3"]
        question_id = question_handler().create_new_record_in_question_tbl(question, question_detail_info, user_id, tag_list)

def question_list():
    """
    test data
    """
    question_list = db(db.question_tbl).select()
    """
    if not len(question_list):
        create_data_for_question_list_for_test()
    """
    """
    end test data
    """
    items= []


    try:
        items = db(db.question_tbl).select()

    except:
        log.error('cant query data from db')
    return dict(items= items, audience_id = '1')

def get_header(text):
    """
        get header of article
    """
    header_position =text.find("<p>&nbsp;</p>")
    log.info("header_position = %d", header_position)
    header_text =  request.vars.editor1[:header_position]
    return header_text





#@auth.requires_login()
def post():
    log.info("request.vars = %s",request.vars)
    session.tag_list_store = []
    return dict(article_tag_list ="" )


@auth.requires_login()
def post_tag():
    session.tag_list_store.append(request.vars.tag_info)
    log.info("session.tag list = %s", session.tag_list_store)
    #return json.dumps(request.vars.tag_info)
    return "var x=$('#target'); x.html(x.html()+' %s');" % request.vars.tag_info.replace("'","\\'")


@auth.requires_login()
def post_question():
    log.info("post")
    log.info("request.vars = %s",request.vars)
    import pdb;pdb.set_trace()
    question_id = post_new_question(request, auth, session)
    if question_id:
        redirect(URL(r = request, f= 'question', args = question_id))
    return dict()


@auth.requires_login()
def user_modify_question():
    update_a_question(request, session.tag_list_store)
    return dict()


####### answer ######

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
    import pdb; pdb.set_trace()
    user_like_a_question(request, auth)
    return "unlike"

@auth.requires_login()
def unlike_a_question():
    user_unlike_a_question(request, auth)
    return "like"






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