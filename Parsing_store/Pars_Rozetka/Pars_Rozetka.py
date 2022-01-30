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


def get_list_category_next(index_link, headers):
    r = request(index_link, headers=headers)
    soup = BeautifulSoup(r,'lxml')
    list_links_category_next = soup.find_all(class_='tile-cats__picture')
    list_link = []
    for i in list_links_category_next[0:18]:
        list_link.append(i.get('href'))
    return list_link


def get_pagination_page_and_soup(page,header):
    r = request(page,headers=header)
    soup = BeautifulSoup(r,'lxml')
    all_pagenation = soup.find_all(class_='pagination__link ng-star-inserted')[-1].text
    return int(all_pagenation)


def get_list_card(link_down_category,header):
    pagenation = get_pagination_page_and_soup(link_down_category,header)
    all_card = []
    print(f'{link_down_category}')
    for i in range(0,pagenation+1):
        link = f'{link_down_category}page={i}/'


    pass

def main():
    headers = config()
    url = "https://rozetka.com.ua/ua/"
    list_links_category = get_list_category(request(url, headers))
    #print(list_links_category[0])
    list_links_category_next = get_list_category_next(list_links_category[0],headers)
    print(list_links_category_next[0])
    print(get_list_card(list_links_category_next[0], headers))

main()
