__author__ = 'mac'


import os


#test user
EMAIL_TEST_USER_1='qcbavsr_sharpestein_1418015926@tfbnw.net'
PASS_TEST_USER_1='maiphuong'

LOCAL_TEST = "http://localhost:8002"
REAL_TEST ="http://testmobileissomuchfun.appspot.com"
BASE_URL = ''
LOGIN_URL = ''
LOGOUT_URL = ''
QUESTION_LIST_URL = ''

NUM_OF_QUESTION_PER_PAGE = 12

def  option_handler(sys):
    global BASE_URL
    global QUESTION_LIST_URL
    global LOGIN_URL
    global LOGOUT_URL
    global FB_PAGE

    try:
        option = sys.argv[1]
    except:
        option = ''
    if option == 'local':
        BASE_URL = LOCAL_TEST
        print '...start testing in local machine'
    elif option == 'real':
        BASE_URL= REAL_TEST
        print'...start testing in real version'
    else:
        print'...undefine option is inputted. LOCAL test is executed'
        global BASE_URL
        BASE_URL = LOCAL_TEST

    QUESTION_LIST_URL = os.path.join(BASE_URL, 'question_list')
    LOGIN_URL = os.path.join(BASE_URL, 'user/login?_next=/')
    LOGOUT_URL = os.path.join(BASE_URL, 'user/logout?_next=/')
    FB_PAGE = os.path.join(BASE_URL,'fb_main')
    return BASE_URL

