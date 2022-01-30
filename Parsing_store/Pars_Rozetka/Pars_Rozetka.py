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


def get_list_category_next(index_link, header):
    r = request(index_link, headers=header)
    soup = BeautifulSoup(r,'lxml')
    list_links_category_next = soup.find_all(class_='tile-cats__picture')
    list_link = []
    for i in list_links_category_next[0:18]:
        print(i)
        list_link.append(i.get('href'))
    print(list_link)

def main():
    headers = config()
    url = "https://rozetka.com.ua/ua/"
    list_links_category = get_list_category(request(url, headers))
    print(list_links_category[0])
    list_links_category_next = get_list_category_next(list_links_category[0],headers)


main()
