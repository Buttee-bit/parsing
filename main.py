from bs4 import BeautifulSoup
import time
import requests
import json
import csv


def get_all_links_all_mark(url):

    headers = config()
    r = requests.get(url, headers=headers).content

    soup = BeautifulSoup(r,'lxml')
    all_links = soup.find('div', class_='IndexMarks').find_all('div',class_='IndexMarks__col')

    all_links_all_marks = []
    all_name_marks = []
    for link in all_links:
        link_mark_column = link.find_all('a',class_='IndexMarks__item')
        for mark in link:
            try:
                name_mark = mark.find('div', class_='IndexMarks__item-name').text
            except:
                name_mark = 'какаято херня'
            # name_mark = mark.find('div',class_='IndexMarks__item-name').text
            link_mark = mark.get('href')
            all_links_all_marks.append(link_mark)
            all_name_marks.append(name_mark)

            
    all_links_all_marks.pop(-1)
    return all_links_all_marks,all_name_marks


def algoritm_data(marks,name_marks):
    for mark,name_mark in zip(marks,name_marks):
        box_mark = []
        pagenation = get_pagination(mark)
        print(f'парсим {name_mark} марку')
        for page_info in range(1, pagenation + 1):
            print(f'Парсим {page_info} осталось {(pagenation+1)-page_info}')
            code_page = get_all_page(page_info,mark)

            info_box = get_info(code_page)
            print(f'парсинг {name_mark} готов на {((page_info)/pagenation)*100}%')
            box_mark.append(info_box)

        save_json_file(box_mark,name_mark)




def config():

    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    return headers


def get_pagination(url):
    headers = config()

    r = requests.get(url, headers=headers).content
    soup = BeautifulSoup(r,'lxml')
    pagenation = int(soup.find('span',class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination-module__pages').find_all('a',class_='Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page')[-1].find('span',class_='Button__text').text)
    return pagenation

def get_all_page(pagenation,mark):
    code_page = requests.get(f"{mark}?page={pagenation}").content
    return code_page

def get_info(page_pagenation):
    alva_digit = '0123456789'
    soup = BeautifulSoup(page_pagenation,'lxml')
    all_car = soup.find('div',class_='thaXCZTq2KU_xDVQ-module__container thaXCZTq2KU_xDVSQNF7NBrRZeM_IArcR').find_all('div',class_="ListingItem-module__container thaXCZTq2KU_xDVSQNF7NBrRZeM_IArcRlDRToLa5bg")
    box_car = []
    for card_car in all_car:
        try:
            name_car = card_car.find('a',class_='Link ListingItemTitle__link').text
        except:
            print('NO DATA')
        try:
            ttx = card_car.find('div',class_='ListingItemTechSummaryDesktop__column').find_all('div',class_='ListingItemTechSummaryDesktop__cell')[0].text
        except:
            print('NO DATA')
        try:
            box_pered = card_car.find('div',class_='ListingItemTechSummaryDesktop__column').find_all('div',class_='ListingItemTechSummaryDesktop__cell')[1].text
        except:
            print('NO DATA')
        try:
            side_and_doors = card_car.find('div',class_='ListingItemTechSummaryDesktop__column').find_all('div',class_='ListingItemTechSummaryDesktop__cell')[2].text
        except:
            print('NO DATA')
        try:
            prize_car = card_car.find('div',class_='ListingItemPrice-module__container ListingItem-module__price').find('span').text
            new_prize = ''
            for j in prize_car:
                if j in alva_digit:
                    new_prize += str(j)
            prize_car = new_prize
        except:
            prize_car = 'данные не получилось собрать'
        try:
            year = card_car.find('div',class_='ListingItem-module__year').text.strip()
        except:
            print('NO DATA')

        box_car.append({

            'Name_car': name_car,
            'ttx_engine': ttx,
            'transmission_box':box_pered,
            'side_and_doors': side_and_doors,
            'prize': prize_car,
            'year': year

        })
    return box_car



def save_json_file(info_box,name):
    file_path = f'data_avito_{name}.json'
    with open(file_path,'w',encoding='utf-8') as f:
        json.dump(info_box, f, indent=4, ensure_ascii=False)

def main():
    start_time = time.time()
    url = 'https://auto.ru/'
    marks,name = get_all_links_all_mark(url)
    algoritm_data(marks,name)
    print("--- %s seconds ---" % (time.time() - start_time))

main()