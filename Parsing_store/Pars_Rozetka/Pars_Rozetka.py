from bs4 import BeautifulSoup
import requests
import csv


def request(url, headers):  # дает код страницы
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    else:
        print('Ошибка подключения')


def config():  # конфигурация к реквест запросу
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36 '
    }
    return headers


def get_list_category(requests_main_page_text):  # дает список ссылок на категории из шлавного меню
    soup = BeautifulSoup(requests_main_page_text, 'lxml')

    category = soup.find_all(class_='menu-categories__link')
    list_category = []
    for i in category[0:19]:  # Костыль именно для этого сайта
        list_category.append(i.get('href'))
    return list_category


def get_list_category_next(index_link, headers):  # Дает лист ссылок в ПОДкатегории
    r = request(index_link, headers=headers)
    soup = BeautifulSoup(r, 'lxml')
    list_links_category_next = soup.find_all(class_='tile-cats__picture')
    list_link = []  # список ссылок на подкатегории
    for i in list_links_category_next[0:18]:  # +- также костыль
        list_link.append(i.get('href'))
    return list_link


#  В этой функции дописать , что если не найдены значения , то забить , там другая структура сайта
def get_pagination_page_and_soup(page, headers):  # Дает интовое значение последней страницы
    r = request(page, headers=headers)
    soup = BeautifulSoup(r, 'lxml')
    try:
        all_pagenation = soup.find_all(class_='pagination__link ng-star-inserted')[
            -1].text  # находим последнию страницу
        return int(all_pagenation)
    except:
        return 1


def get_list_page_card(link_down_category, headers):  # с i'той страницы собирает ссылки на все карторчки товара
    pagenation = get_pagination_page_and_soup(link_down_category, headers)
    list_page_card = []  # Находим все ссылки карточек на странице
    # print(f'{link_down_category}')
    for i in range(1, pagenation + 1):
        link = f'{link_down_category}page={i}/'  # Преобразовываем ссылку для работы с пагинациями
        list_page_card.append(link)
    return list_page_card


def get_open_card(list_page_card, headers):  # Открываем карточку продукта с листа страницы
    r = request(list_page_card, headers=headers)
    soup = BeautifulSoup(r, 'lxml')
    all_card = soup.find_all(class_='goods-tile__picture ng-star-inserted')
    list_cards_link = []
    for i in all_card:
        list_cards_link.append(i.get('href'))
    return list_cards_link


def get_content(list_cards_link, headers):  # Получаем информацию с карточки
    r = request(list_cards_link, headers=headers)
    soup = BeautifulSoup(r, 'lxml')
    product = []
    # тут находим то что надо
    name = soup.find_all(class_='product__title')[0].text
    try:
        price = soup.find_all(class_='product-prices__big product-prices__big_color_red')[0].text
        price = get_only_digit(price)
    except:
        price = soup.find_all(class_='product-prices__big')[0].text
        price = get_only_digit(price)
    info = soup.find_all(class_='product-about__brief ng-star-inserted')[0].text
    # Тут добавляем то что надо
    product.append({
        'name': name,
        'price': price,
        'info': info
    })
    return product


def get_only_digit(soup_obj):
    digit = '0123456789'
    only_digit = ''
    for i in soup_obj:
        if i in digit:
            only_digit += i
    return only_digit + ' гривней'


def save_info_next_category(name_category, data):
    name_category = 'data_Rozetka/' + name_category.split('/')[-3]
    data_head = ['name', 'price', 'info']
    print(name_category)
    with open(f'{name_category}.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data_head)
        for item in data:
            try:
                writer.writerow(
                    [item['name'], item['price'], item['info'], ])
            except:
                pass


def main():
    headers = config()
    url = "https://rozetka.com.ua/ua/"
    list_links_category = get_list_category(request(url, headers))
    for category in list_links_category[0:2]:  # Проходимся по категория в списке ссылок категорий
        try:
            list_links_category_next = get_list_category_next(category,
                                                              headers)  # Получаем список ссылок на подгатегории
        except:
            pass
        for next_category in list_links_category_next[0:2]:  # Из всех подкатегории проходимся по всем
            try:
                list_page_card = get_list_page_card(next_category, headers)
            except:
                pass
            for page in list_page_card[0:2]:
                print(page)
                list_cards_link = get_open_card(page, headers)
                for card in list_cards_link[0:1]:
                    print(card)
                    try:
                        card_info = get_content(card, headers)
                    except:
                        pass
                    print('Сохраняем данные...')
                    save_info_next_category(next_category, card_info)


main()
