__author__ = 'mac'
class QuestionList():
    def questionElement(self, question_info, driver):
        try:
            tag_info = question_info.find_element_by_class_name('article_tag')
            question_unit = question_info.find_element_by_class_name('article_header')
            question_detail_info = question_info.find_element_by_class_name('article_introduction')
            popularity_info = question_info.find_element_by_class_name('article_popularity_info')
            register_to_like = popularity_info.find_element_by_class_name('register_to_like')
            count_like= popularity_info.find_element_by_class_name('count_like')
            answer_info= popularity_info.find_element_by_class_name('popularity_a_tag_text')
            user_profile= popularity_info.find_element_by_id('user_profile')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()
            return True
        except:
            return False

class QuestionPage():
    """
    Define element in Question Page
    """
    def questionElement(self):
        #check if no answer button is there
        try:
            tag_info = self.driver.find_element_by_class_name('article_tag')
            question_info=self.driver.find_element_by_class_name('article_header')
            question_detail_info=self.driver.find_element_by_class_name('article_introduction')
            popularity_info=self.driver.find_element_by_class_name('article_popularity_info')
            user_profile = popularity_info.find_element_by_id('author_profile')
        except:
            return False
        return True
        #click on  question on right side bar
        """
        side_bar_questions = self.driver.find_element_by_id('right_bar_question_list')
        question = side_bar_questions.find_element_by_id('related_question')
        question.click()
        self.driver.back()
        """
    def answerElement(self, answer_info):
        """
        check element of answer
        """
        try:
            user_info = self.driver.find_element_by_class_name('user_info')
            user_profile = user_info.find_element_by_id('user_profile')
            user_detail_info = user_info.find_element_by_class_name('user_detail_info')
            comment_info = answer_info.find_element_by_class_name('comment_info')
            popularity_info = answer_info.find_element_by_class_name('article_popularity_info')
            count_like_info = popularity_info.find_element_by_class_name('count_like')
            register_to_like = popularity_info.find_element_by_class_name('register_to_like')
        except:
            return False
        return True



class ProfilePage():
    """
    User profile page
    """
    def userProfileElement(self):
        try:
            user_name = self.driver.find_element_by_class_name('user_fb_name')
            question_info=self.driver.find_element_by_class_name('user_detail_info')

        except:
            return False
        return True
    def questionElement(self, question_info, driver):
        try:
            question_unit = question_info.find_element_by_class_name('article_header')
            answer_info = question_info.find_element_by_class_name('user_detail_info')
            link = question_unit.find_element_by_link_text(question_unit.text)
            link.click()
            driver.back()
            return True
        except:
            return False