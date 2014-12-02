__author__ = 'huyheo'

#python applications/chuotnhat/funtionalTest/testUnloginUser.py

import unittest
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import *
import os, sys
import string, random



class TagUtility(object):
    """
    tool for handling user tag info
    """
    INPUT_TAG_BOX = 'typing_box'
    SUGGESTION_BOX = 'suggestion_box'
    SAVE_TAG_LIST = 'save_tag_list_button'
    def __init__(self, driver):
        self.driver = driver


    def delete_all_user_tag_info(self):
        tag_list = self.driver.find_elements_by_class_name('post-tag')
        if len(tag_list):
            for tag_unit in tag_list:
                tag_del_but = tag_unit.find_element_by_id('delete_tag')
                tag_del_but.click()
            save_button = self.driver.find_element_by_id('save_tag_list_button')
            save_button.click()


    def add_new_tag(self, tag_name):
        tag_info= self.driver.find_element_by_id(self.INPUT_TAG_BOX)
        tag_info.click()
        tag_info.send_keys(tag_name)
        sleep(2)
        temp = self.driver.find_element_by_id(self.SUGGESTION_BOX)
        temp.click()
        sleep(1)

    def add_new_tags(self, tag_list):
        for tag_info in tag_list:
            self.add_new_tag(tag_info)

        save_button = self.driver.find_element_by_id(self.SAVE_TAG_LIST)
        save_button.click()

    def get_tag_suggestion(self, input_tag):
        tag_info= self.driver.find_element_by_id(self.INPUT_TAG_BOX)
        tag_info.click()
        sleep(1)
        tag_info.send_keys(input_tag)
        sleep(2)
        temp = self.driver.find_element_by_id(self.SUGGESTION_BOX)
        tag_suggess = temp.find_elements_by_xpath('div')
        tag_suggess_list = []
        for data in tag_suggess:
            tag_suggess_list.append(data.text)
        return tag_suggess_list

    def get_added_tag(self):
        tag_list = self.driver.find_elements_by_class_name('post-tag')
        tag_added_list = []
        if len(tag_list):
            for tag_unit in tag_list:
                tag_added_list.append(tag_unit.text[:len(tag_unit.text)-1])
        return tag_added_list


class HandlingQuestion(unittest.TestCase):
    POST_BUTTON_ID = "post_button"
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.question_info = 'this is a question'
        self.edit_question_info = 'this is a edited question'
        self.question_info_detail = ' this is a detail of question'
        self.edited_question_info_detail = ' this is a detail of question'


    def compose_post(self):
        driver = self.driver
        try:
            post_button = driver.find_element_by_id(self.POST_BUTTON_ID)
            post_button.click()
        except:

            sleep(2)
            post_button = driver.find_element_by_id(self.POST_BUTTON_ID)
            post_button.click()

        #add tag
        sleep(2)
        tag_info= driver.find_element_by_id('month')
        tag_info.click()
        tag_info.send_keys('c')
        try:
            sleep(1)
            temp = driver.find_element_by_id('suggestion_box')
        except:
            #wait for ajax call to finish
            print 'cant receive suggestion box..sleep for 6 second and check again'
            sleep(6)
            temp = driver.find_element_by_id('suggestion_box')
        tag_suggess = temp.find_element_by_xpath('div')
        tag_suggess.click()
        #post_tag_button = driver.find_element_by_id('submit1')
        #post_tag_button.click()
        #add question title
        question_info = driver.find_element_by_id('question_header')
        question_info.clear()
        question_info.send_keys(self.question_info)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.question_info_detail))

    def post(self):
        self.compose_post()
        submit_button = self.driver.find_element_by_id('post_question_button')
        submit_button.click()


    def delete_post(self):
        #delete post
        driver = self.driver
        delete_button = driver.find_element_by_id('delete_button')
        delete_button.click()
        yes_selection = driver.find_element_by_id('yes_selection')
        yes_selection.click()

    def edit_post(self):
        driver = self.driver
        edit_button = driver.find_element_by_id('edit_button')
        edit_button.click()
        question_info = driver.find_element_by_id('question_header')
        question_info.clear()
        question_info.send_keys(self.edit_question_info)
        #wait a bit for javascript to load to use tinymce api
        sleep(5)
        driver.execute_script("tinymce.get('{0}').focus()".format('editor1'))
        driver.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(self.edited_question_info_detail))
        submit_button = driver.find_element_by_id('post_question_button')
        submit_button.click()





    def tearDown(self):
        self.driver.close()

