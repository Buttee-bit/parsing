from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

user = 'bstislavsk_' # Имя нашего пользователя
userPassword = 'FreeRollPlay' # Наш пароль
browser = webdriver.Chrome('chromedriver.exe')


def loqin(user,userPassword):
    browser.get('https://www.instagram.com/')

    try:
        time.sleep(random.randint(1,3))

        userNameInput = browser.find_element(By.NAME,'username')
        userNameInput.clear()
        userNameInput.send_keys(user)

        time.sleep(random.randint(1,3))

        userPassworInput = browser.find_element(By.NAME,'password')
        userPassworInput.clear()
        userPassworInput.send_keys(userPassword)

        userPassworInput.send_keys(Keys.ENTER)
        time.sleep(4)


    except Exception as exp:
        print (exp)
        browser.close()
        browser.quit()

def hastag_search_like(hastag,match):
    try:
        browser.get(f'https://www.instagram.com/explore/tags/{hastag}/')
        time.sleep(3)

        linksHastag = browser.find_elements(By.TAG_NAME,'a')
        posts_links = []
        for link in linksHastag:
            href = link.get_attribute('href')#

            if '/p/' in href:
                posts_links.append(href)
                print(href)

        for i in range(match):

            browser.get(posts_links[i])
            time.sleep(3)
            likeButton = browser.find_elements(By.CLASS_NAME,'wpO6b  ')[1].click()
            time.sleep(2)

        browser.close()
        browser.quit()
    except Exception as exp:
        print (exp)

loqin(user,userPassword)
hashtag = 'girls'
match = 3
hastag_search_like(hashtag,match)