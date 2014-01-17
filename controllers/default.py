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

log = logging.getLogger("h")
log.setLevel(logging.DEBUG)

from ConstantDefinition import *

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

def article_list():
    items= []

    try:
        items = db(db.question_tbl).select()

    except:
        log.error('cant query data from db')

    for item in items:
        log.info('items = %s',item)
        comment_count = db(db.comment_tbl.id == item.id).select()
        log.info('comment_count = %d', len(comment_count))
        tag_list = db(db.tag_tbl.question_info ==item.id).select()
        log.info('tag_list = %d', len(tag_list))
        for tag in tag_list:
            tag_name = db(db.article_tag.id == tag.tag_info).select()[0]
            log.info('tag_name = %s', tag_name)
    return dict(items= items)

def get_header(text):
    """
        get header of article
    """
    header_position =text.find("<p>&nbsp;</p>")
    log.info("header_position = %d", header_position)
    header_text =  request.vars.editor1[:header_position]
    return header_text


def post_article_class():
    log.info("request.vars = %s",request.vars.article_class)
    article_classes = request.vars.article_class
    article_class_list = db(db.article_class).select()
    log.info("article = %s ",article_class_list )


    result= ""
    if len(article_classes):
        for item in article_classes:
            log.info("item = %s", item)
            try:
                db(db.article_class.id == article_class_list[article_classes.index(item)].id).update(name=item)
            except:
                log.error("database error")
                result = "failure"
    else:
        log.error("no infor about article class")

    result = "update article class successfully"

    return dict(result = result)




def article_class():
    """
        Create, change , update article_class
    """
    article_class_list = db(db.article_class).select()
    log.info("article_class = %s", article_class_list.__doc__ )

    if len(article_class_list) > 0:
            log.info(" article class is existed..display it")
    else:
        log.info("create database:w")
        #create database
        db.article_class.insert(name ="")
        db.article_class.insert(name ="")
        db.article_class.insert(name ="")
        db.article_class.insert(name ="")

    article_class_list = db(db.article_class).select()
    log.info("article_class = %s", article_class_list )
    return dict(article_class_list = article_class_list)

def get_article_id(name):
    """
    return id
    """
    article_class_list = db(db.article_tag).select()
    log.info("article_class = %s", article_class_list)
    for item in article_class_list:
        if item.name == name:
            return item.id
    return False;


@auth.requires_login()
def post():
    article_tag_list = db(db.article_tag).select()
    log.info("article_tag = %s", article_tag_list)

    return dict(article_tag_list =article_tag_list )


@auth.requires_login()
def post_article():
    log.info("post")
    log.info("request.vars = %s",request.vars)
    article_class = request.vars.article_class
    header_text = request.vars.article_header
    introduction_text  = request.vars.article_introduction
    content_text = request.vars.editor1

    log.info("session.user = %s", auth.user)
    log.info("header_text = %s", header_text)
    log.info("auth.user.id = %s", auth.user.id)


    articleId = get_article_id(article_class)

    if articleId == False:
        log.error('cant get article id')
    """
    question_tbl_list= db(db.question_tbl).select()
    log.info("question_tbl_list = %s", question_tbl_list)
    """
    question_id =""

    try:
        question_id = db.question_tbl.insert(story = content_text,
                                article_introduction = introduction_text,
                                article_header = header_text,
                                writer = auth.user.id)
        log.info('successfully create a question_tbl')


    except:
        log.error('cant create question_tbl')
    try:
        tag_id = db.tag_tbl.insert(tag_info = articleId,
                            question_info = id_temp)
    except:
        log.error('cant create tag for question')
    redirect(URL(r = request, f= 'article', args = question_id))
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