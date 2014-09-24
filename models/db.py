# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################


if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
from gluon import current
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:12660f29-c206-409f-8215-ed11cc55ccf2'   # before define_tables()
# define the auth_table before call to auth.define_tables()
auth_table = db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=""),
    Field('last_name', length=128, default=""),
    #Field('username', length=128, default="", unique=True),
    Field('email', length=128, default=''),
    Field('username', length=128, default=""),
    Field('password', 'password', length=256,
          readable=False, label='Password'),
    Field('registration_id', length=128, default= "",
          writable=False, readable=False))

auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)

auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

crud.settings.auth = None                      # =auth to enforce authorization on crud

################################################################################
## use fb auth
## for facebook "graphbook" application
################################################################################

current.db = db
current.auth = auth
#extend information for auth_user
db.define_table('user_profile',
    Field('user_info', 'reference auth_user'),
    Field('sub_info','text'),
    Field('detail_info','text'))

db.define_table('question_tbl',
    Field('question_info', 'text'),
    Field('question_detail_info', 'text'),
    Field('writer', 'reference auth_user'))

db.define_table('question_like_tbl',
    Field('question_id', db.question_tbl),
    Field('user_info','reference auth_user')
    )
db.define_table('question_follow_tbl',
    Field('question_id', db.question_tbl),
    Field('user_info','reference auth_user')
)
db.define_table('question_report_tbl',
    Field('question_id', db.question_tbl),
    Field('user_info','reference auth_user')
)



#store tag of a given question
db.define_table('tag_tbl',
                Field('name', 'string')
)
db.define_table('question_tag_tbl',
    Field('question_info',db.question_tbl),
    Field('tag_info', db.tag_tbl))



# answer tables
db.define_table('answer_tbl',
    Field('answer_info', 'text'),
    Field('question_id',db.question_tbl),
    Field('author_info', 'reference auth_user'))

db.define_table('answer_like_tbl',
    Field('answer_id', db.answer_tbl),
    Field('user_info','reference auth_user'))

db.define_table('answer_report_tbl',
    Field('answer_id', db.answer_tbl),
    Field('user_info', 'reference auth_user'))


# follower feature
db.define_table('follow_info_tbl',
    Field('followed_user', 'reference auth_user'),
    Field('following_user', 'reference auth_user'))


import sys, os
path = os.path.join(request.folder, 'modules')
if not path in sys.path:
    sys.path.append(path)

from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount
class FaceBookAccount(OAuthAccount):
    """OAuth impl for FaceBook"""
    AUTH_URL="https://graph.facebook.com/oauth/authorize"
    TOKEN_URL="https://graph.facebook.com/oauth/access_token"

    def __init__(self, g):

        OAuthAccount.__init__(self, g, "228859397308903", "650209bd438e288908309751aae01b5d",
                              self.AUTH_URL, self.TOKEN_URL,
                              scope='user_photos,friends_photos')
        self.graph = None


    def get_user(self):
        '''Returns the user using the Graph API.
        '''
        if not self.accessToken():
            print' return none'
            return None

        if not self.graph:
            self.graph = GraphAPI((self.accessToken()))

        user = None
        try:
            user = self.graph.get_object("me")
        except GraphAPIError, e:
            self.session.token = None
            self.graph = None

        if user:

            first_name = user['first_name']
            last_name = user['last_name']
            username = user['id']
            #email = user['email']

            return dict(first_name = user['first_name'],
                        last_name = user['last_name'],
                        #email    = user['email'],
                        username = user['id'])


crud.settings.auth = None                      # =auth to enforce authorization on crud
auth.settings.actions_disabled=['register','change_password','request_reset_password','profile']
auth.settings.login_form=FaceBookAccount(globals())
#auth.settings.login_next=URL(f='index')
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
