from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

user = 'bstislavsk_'
userPassword = 'FreeRollPlay'

def loqin(user,userPassword):
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get('https://www.instagram.com/')
    try:
        time.sleep(random.randint(3,5))


        userNameInput = browser.find_element_by_name('username')
        userNameInput.clear()
        userNameInput.send_keys(user)

        time.sleep(random.randint(1,3))

        userPassworInput = browser.find_element_by_name('password')
        userPassworInput.clear()
        userPassworInput.send_keys(userPassword)

        userPassworInput.send_keys(Keys.ENTER)
        time.sleep(10)





        browser.close()
        browser.quit()
    except Exception as exp:
        print (exp)
        browser.close()
        browser.quit()
loqin(user,userPassword)