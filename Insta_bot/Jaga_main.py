from colorama import init
from colorama import Fore
from selenium.webdriver.common.by import By
import selenium

LOGIN = ''
PASSWORD = ''


def main():
    init(autoreset=True)

    nickname = input("Enter nickname - ")
    driver = selenium.webdriver.Chrome()

    driver.get(f'https://www.instagram.com/{nickname}/')

    # driver.implicitly_wait(30)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(LOGIN)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.get(f'https://www.instagram.com/{nickname}/')

    name = driver.find_element(By.XPATH, '//div[@class="QGPIr"]/h1').text
    print(f"Name - {name}")

    try:
        biography = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/span').text
        if biography == "":
            print("Biography - " + Fore.RED + "User haven't biography")
        print(f"Biography - {biography}")
    except:
        print("Biography - " + Fore.RED + "User haven't biography")

    followers = driver.find_elements(By.XPATH, '//span[@class="g47SY "]')[1].text
    print("Followers - " + followers)

    following = driver.find_elements(By.XPATH, '//span[@class="g47SY "]')[2].text
    print("Following - " + following)

    try:
        driver.find_element(By.XPATH, '//div[@class="_4Kbb_ _54f4m"]')
        private_account = True
    except:
        private_account = False

    if private_account:
        print("Account is " + Fore.RED + "close")
    else:
        print("Account is " + Fore.LIGHTCYAN_EX + "open")

    try:
        driver.find_element(By.XPATH, '//span[@class="mTLOB Szr5J coreSpriteVerifiedBadge "]')
        verified_account = True
    except:
        verified_account = False

    if verified_account:
        print("Account " + Fore.LIGHTCYAN_EX + "Verified")
    else:
        print("Account " + Fore.RED + "Not Verified")

    driver.quit()


if __name__ == "__main__":
    main()