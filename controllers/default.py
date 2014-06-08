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

def month_selector():
    if not request.vars.tag_info: return ''
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September' ,'October',
              'November', 'December']
    month_start = request.vars.tag_info.capitalize()
    selected = [m for m in months if m.startswith(month_start)]
    return DIV(*[DIV(k,
                     _onclick="jQuery('#month').val('%s')" % k,
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for k in selected])



def user():
    return dict(form = auth())

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #redirect(URL(r = request, f= 'blog', args = 3))
    user = auth.user
    print user
    return dict()

def post_question():
    data_group = [{'type':'now',"data":""},{'type':'future',"data":""}]
    return json.dumps(data_group)




def article():
    """
    Display blog by id
    """
    log.info("request.vars = %s", request.args[0])
    log.info("request.vars = %s",request.vars)



    if request.args[0] == 'post_comment':
        log.info('post a comment')
        post_comment(request.vars.questionId, request.vars.editor1, auth.user.id)
        redirect(URL(r = request, f= 'article', args = request.vars.questionId))

    else:
        log.info('show article with comment')
        log.info('id = %s', request.args[0])

        try:
            question = db(db.question_tbl.id == int(request.args[0])).select()[0]
        except:
            log.error('cant query a blog from db')
            question = None
        comment_list = show_question(request.args[0])

        return dict(item = question, comment_list = comment_list)


def show_question(question_id):

    comment_list = db(db.comment_tbl.question_info == question_id).select()
    return  comment_list


def post_comment(question_id, comment_info, user_id):
    log.info("post_comment")

    log.info("session.user = %s", auth.user)
    log.info("auth.user.id = %s", user_id)



    try:
        comment_id = db.comment_tbl.insert(comment_info = comment_info,
                                question_info = question_id,
                                author_info = user_id
                                )
        log.info('successfully create a comment_tbl')


    except:
        log.error('cant create comment_tbl')


@auth.requires_login()
def edit_article():
    """
    Edit blog
    """
    log.info("edit artchile")
    log.info("request.vars 0= %s", request.args[0])
    log.info("request.vars = %s", request.args)
    id_info = request.args[0]

    article_class_list = db(db.article_tag).select()
    log.info("article_class = %s", article_class_list)

    try:
        blog_item = db(db.blog.id == int(id_info)).select()[0]
    except:
        log.error('cant query a blog from db')
        blog_item = None



    if request.vars.editor1:
        article_id = get_article_id(request.vars.article_class)
        log.info("article-id = %s", article_id)
        id =db(db.blog.id == int(request.args[0])).update(
            article_type = article_id,
            article_header = request.vars.article_header,
            article_introduction = request.vars.article_introduction,
            story = request.vars.editor1
        )
        redirect(URL(r = request, f= 'article', args = [request.args[0]]))

    log.info("blog_item = %s",blog_item)
    return dict(article = blog_item, article_class_list = article_class_list)

        
def delete_article():
    selection = request.vars
    log.info('selection = %s', selection['selection'])
    log.info('id = %s', request.args[0])
    id_info = request.args[0]
    if selection['selection'] == "YES":
        log.info("delete post")
        db(db.question_tbl.id == int(request.args[0])).delete()
        redirect(URL(r = request, f= 'article_list'))
    elif selection['selection'] == "NO":
        redirect(URL(r = request, f= 'article', args = [request.args[0]]))
    return dict()

def question_list():
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





#@auth.requires_login()
def post():
    log.info("request.vars = %s",request.vars)
    session.tag_list_store = []
    return dict(article_tag_list ="" )


@auth.requires_login()
def post_tag():
    log.info("post_tag")
    log.info("request.vars = %s",request.vars.tag_info)
    session.tag_list_store.append(request.vars.tag_info)
    log.info("session.tag list = %s", session.tag_list_store)
    #return json.dumps(request.vars.tag_info)
    return "var x=$('#target'); x.html(x.html()+' %s');" % request.vars.tag_info.replace("'","\\'")


@auth.requires_login()
def post_question():
    log.info("post")
    log.info("request.vars = %s",request.vars)

    question_id = post_new_question(request, auth)
    if question_id:
        redirect(URL(r = request, f= 'article', args = question_id))
    return dict()


@auth.requires_login()
def user_delete_question():
    delete_a_question(request)
    return dict()
@auth.requires_login()
def user_modify_question():
    update_a_question(request)
    return dict()


####### answer ######
@auth.requires_login()
def user_post_new_answer():
    create_new_answer(request, auth)
    return dict()

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
def user_like_a_question():
    like_a_question(request, auth)
    return dict()

@auth.requires_login()
def user_unlike_a_question():
    unlike_a_question(request, auth)
    return dict()






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