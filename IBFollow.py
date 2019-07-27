from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys

class pynstaBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(3)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(3)

    def follow(self, hashtag):

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        pic_hrefs = []
        for i in range(1, 2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        unique_photos = len(pic_hrefs)
        likeCounter = 0
        followCounter = 0
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(220, 323))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                follow_button = driver.find_element_by_xpath("//button[contains(., 'Follow')]").click()
                # find_user = driver.find_element_by_xpath('//a[@class="FPmhX"]')
                # print(str(find_user))
                likeCounter += 1
                print(str(likeCounter) + " photos liked.")

                followCounter += 1
                print(str(followCounter) + " profiles followed.")

                like_button().click()
                # find_user().click()
                time.sleep(2)
                follow_button().click()

            except Exception as e:
                time.sleep(10)
            unique_photos -= 1

if __name__ == "__main__":

    username = "yourUserName"
    password = "yourPassword"

    ig = pynstaBot(username, password)
    ig.login()

    hashtags = []
    f = open('hashtags.txt', 'r')
    x = f.readlines()
    f.close()
    for line in x:
        hashtags.append(line)

    notFollowedBack = []
    f = open('notFollowedBack.txt', 'r')
    x = f.readlines()
    f.close()
    for line in x:
        notFollowedBack.append(line)

    while True:
        try:
            tag = random.choice(hashtags)
            ig.follow(tag)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = pynstaBot(username, password)
ig.login()