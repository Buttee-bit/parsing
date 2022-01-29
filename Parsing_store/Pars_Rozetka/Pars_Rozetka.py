from bs4 import BeautifulSoup
import requests
import csv


def request(url, headers):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    else:
        print('Ошибка подключения')


def config():
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    return headers


def get_list_category(requests_main_page_text):
    soup = BeautifulSoup(requests_main_page_text, 'lxml')

    category = soup.find_all(class_='menu-categories__link')
    list_category = []
    for i in category[0:19]:
        list_category.append(i.get('href'))
    return list_category

def main():
    headers = config()
    url = "https://rozetka.com.ua/ua/"
    get_list_category(request(url, headers))


main()
