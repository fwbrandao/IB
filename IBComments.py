import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class Commenter:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(750, 900)

    def closeBrowser(self):
        self.driver.close()

    """Login"""

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        user_name_elem = driver.find_element_by_xpath(
            "//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)

        passworword_elem = driver.find_element_by_xpath(
            "//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)

        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(5)

    """getting pics on the hashtag"""

    def get_pictures_on_page(self, hashtag, scrolls=int):

        self.driver.get(
            "https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gather photos
        pic_hrefs = []
        for i in range(1, scrolls):
            try:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if hashtag in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href)
                 for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue
            return pic_hrefs

    """write comment in text area using lambda function"""

    """write comment in text area using lambda function"""
    def write_comment(self, comment_text):
        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    """Actually post a comment"""
    def post_comment(self, comment_text):
        time.sleep(random.randint(1,5))

        comment_box_elem = self.write_comment(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Submit']")
                post_button().click()
                print('clicked post button')
            except NoSuchElementException:
                pass

        time.sleep(random.randint(4, 6))
        self.driver.refresh()
        if comment_text in self.driver.page_source:
            return True
        return False

    """grab comments from a picture page"""
    def get_comments(self):
        # load more comments if button exists
        time.sleep(3)

        try:
            comments_block = self.driver.find_element_by_class_name('Mr508')
            comments_in_block = comments_block.find_elements_by_class_name('gElp9')
            comments = [x.find_element_by_tag_name('span') for x in comments_in_block]
            user_comment = re.sub(r'#.\w*', '', comments[0].text)

        except NoSuchElementException:
            return 'none'
        return user_comment

com = Commenter(username='', password='')
com.login()
# pictures_on_page = com.get_pictures_on_page(hashtag='london', scrolls=3)[1:]
# print(pictures_on_page)
time.sleep(3)
com.driver.get(
    'https://www.instagram.com/p/ByaA7n5H_GN/?taken-by=yourUserName')
time.sleep(3)
# com.write_comment('Big boy, I love you.')
# com.post_comment('Big boy, I love you.')
print(com.get_comments())
