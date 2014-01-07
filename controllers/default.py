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
    redirect(URL(r = request, f= 'blog', args = 3))


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


@auth.requires_login()
def post():
    log.info("post")
    log.info(" request.vars.editor1 = %s", request.vars.editor1)
    log.info("session.user = %s", auth.user)
    test = request.vars.editor1
    try:
        if  test:
            id = db.blog.insert(story = request.vars.editor1,
                            writer = auth.user.id)
            log.info('successfully create a blog')
    except:
        log.error('cant create blog')
    return dict()
