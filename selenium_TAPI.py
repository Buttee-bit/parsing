from selenium import webdriver
import time
from fake_useragent import UserAgent
import random



# options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={ua.random}')


# driver = webdriver.Chrome(executable_path=r'C:\Users\79219\.spyder-py3\chromedriver.exe',
#                           options=options)

# def main():
#     try:
#         driver.get(url=url)
#         next_port = driver.find_elements_by_xpath('//*[@id="content"]/table[2]/tbody/tr/td[2]/div/a/img')[-1]
#         time.sleep(3)
#         next_port.click()
#         next_port = driver.find_elements_by_xpath('//*[@id="content"]/table[2]/tbody/tr/td[2]/div/a/img')[-1]
#         time.sleep(3)
#         next_port.click()
#         next_port = driver.find_elements_by_xpath('//*[@id="content"]/table[2]/tbody/tr/td[2]/div/a/img')[-1]
#         time.sleep(3)
#         next_port.click()



#     except Exception as ex:
#         print(ex)
#     pass
# main()


def create_user():
    options = webdriver.ChromeOptions()
    ua  = UserAgent()
    options.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(executable_path=r'C:\Users\79219\.spyder-py3\chromedriver.exe',
                          options=options)                    
    return driver

def get_page(url, port):
    driver = create_user()
    driver.get(url+port)
    fuck_loqik(driver)
    
def fuck_loqik (driver):
   ports_info = driver.find_elements_by_class_name('port')
   for i in ports_info:
       count = 0
       text_port = i.text
       if count == 0:
           print("ebaboba"+text_port+"ebaboba")
           break
    
def main():
    url = 'https://www.speedguide.net/port.php?port='
    port = 20
    get_page(url=url,port=str(port))

main()