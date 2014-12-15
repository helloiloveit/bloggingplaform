__author__ = 'mac'


import os

LOCAL_TEST = "http://localhost:8002"
REAL_TEST ="http://chuotnhat.vn"
#BASE_URL = REAL_TEST
BASE_URL = LOCAL_TEST
LOGIN_URL = os.path.join(BASE_URL, 'user/login?_next=/')
LOGOUT_URL = os.path.join(BASE_URL, 'user/logout?_next=/')
QUESTION_LIST_URL = os.path.join(BASE_URL, 'question_list')

NUM_OF_QUESTION_PER_PAGE = 12

def  option_handler(sys):
    BASE_URL = LOCAL_TEST
    try:
        option = sys.argv[1]
    except:
        option = ''
    if option == 'local':
        BASE_URL = LOCAL_TEST
        print '...start testing in local machine'
    elif option == 'real':
        BASE_URL = REAL_TEST
        print'...start testing in real version'
    else:
        print'...undefine option is inputted. LOCAL test is executed'
        BASE_URL = LOCAL_TEST


    return BASE_URL

