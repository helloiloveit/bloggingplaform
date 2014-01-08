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

def blog():
    """
    Display blog by id
    """
    log.info("request.vars = %s", request.args[0])
    id_info = request.args[0]

    try:
        blog_item = db(db.blog.id == int(id_info)).select()[0]
    except:
        log.error('cant query a blog from db')
        blog_item = None

    return dict(item = blog_item)

def edit_blog():
    """
    Edit blog
    """
    item_info = blog()
    item = item_info["item"]

    # if user press submit editted blog
    if request.vars.editor1:
        id =db(db.blog.id == int(request.args[0])).update(story = request.vars.editor1)
        redirect(URL(r = request, f= 'blog', args = [request.args[0]]))



    return dict(item = item)
        


def blog_list():
    try:
        items = db(db.blog).select()
        return dict(items = items)
    except:
        log.error('cant query data from db')
        return dict()

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
    log.info("article_class = %s", article_class_list)
    if len(article_class_list) <= 0:
        article_class_list = ["","","",""]

    return dict(article_class_list = article_class_list)

@auth.requires_login()
def post():
    article_class_list = db(db.article_class).select()
    log.info("article_class = %s", article_class_list)

    return dict(article_class_list =article_class_list )


def post_article():
    log.info("post")
    log.info("request.vars = %s",request.vars)
    article_class = request.vars.article_class
    header_text = ""
    content_text = request.vars.editor1
    if isinstance(request.vars.editor1,str):
        header_text = get_header(content_text)
    else:
        log.error("Article has no text")
        return dict()

    log.info("session.user = %s", auth.user)
    log.info("header_text = %s", header_text)
    log.info("auth.user.id = %s", auth.user.id)

    article_class_list = db(db.article_class.id).select()
    log.info("article_class = %s", article_class_list)
    try:
        if  test:
            id = db.blog.insert(story = request.vars.editor1,
                                header = header_text,
                                article_type = article_class,
                            writer = auth.user.id)
            log.info('successfully create a blog')
    except:
        log.error('cant create blog')
    return dict()
