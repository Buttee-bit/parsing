# Импортируем необходимые библиотеки
import requests
from bs4 import BeautifulSoup
import json
import random
import time
from fake_useragent import UserAgent
import csv
# Создаем класс
class Parsing_Aukz:
    def __init__(self,name,link):
        self.name = name
        self.link = link
        print(f'Создан {self.name} парсер')

    def get_fake_UserAgent(self):
        fake_UserAgent = UserAgent().chrome
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': fake_UserAgent
        }
        return headers

    def get_reguest(self,link,fake_UserAgent,i,count,match):

            r = requests.get(f'{link+str(i)}',fake_UserAgent)

            print(f'{count} страница скачана! Осталось: {(match//20)-count} страниц')
            print(f'Готово {count} из {match//20}')
            time.sleep(0.5)
            page = r.text
            self.save_html_page(page,count)

    def save_html_page(self,page,count):
        with open(f"data_aukz/data_page_{str(count)}.html", 'w', encoding='utf-8') as file:
            file.write(page)

    def open_file(self,page_data):
        with open(page_data,'r',encoding='utf-8') as file:
            page = file.read()
            return page

    def get_content(self,page_data):
        page = self.open_file(page_data)
        soup = BeautifulSoup(page,'lxml')
        all_cards = soup.find_all('table')[4]
        box = []
        for card in all_cards:
            try :
                name = card.find_all('td')[2].text
                years = card.find_all('td')[3].text
                words = card.find_all('td')[4].text
                metall = card.find_all('td')[5].text
                report = card.find_all('td')[6].text
                lider = card.find_all('td')[7].text
                match_ctav = card.find_all('td')[8].text
                prize = card.find_all('td')[9].text


                box.append({

                    'Название': name,
                    'Год': years,
                    'Буквы': words,
                    'Металл': metall,
                    'Состояние': report,
                    'Лидер': lider,
                    'Количество ставок': match_ctav,
                    'Актуальная цена': prize
                })

            except:
                print()

        return box
    def save_json_file(self,data,file_path): # Сохраняем результат в json
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(data,f, indent=4, ensure_ascii=False )

    def save_csv_file(self,path,data,data_head):
        with open(path,'w',newline='') as file:
            writer = csv.writer(file,delimiter=';')
            writer.writerow(data_head)
            for item in data:
                writer.writerow([item['Название'],item['Год'],item['Буквы'],item['Металл'],item['Состояние'],item['Лидер'],item['Количество ставок'],item['Актуальная цена'],])
        


    def main(self):
        match = int(input('Введите количество страниц\n'))
        match *= 20
        count = 1
        content = []
        data_head = ['Название','Год','Буквы','Металл','Состояние','Лидер','Количество ставок','Актуальная цена']
        for i in range(0,match,20):
            fake_UserAgent = self.get_fake_UserAgent()
            self.get_reguest(self.link,fake_UserAgent,i,count,match)
            content += self.get_content(f'data_aukz/data_page_{count}.html')
            count += 1
        self.save_json_file(content, f'data_aukz_json/page_aukz_.json')
        self.save_csv_file(f'data_aukz_csv/data.csv',content,data_head)




name = 'Дедушкин парсер'
link = 'http://www.auction.spb.ru/?auctID=338&catID=&order=numblot&foll=&p='

Dadyshkagoga = Parsing_Aukz(name,link)
Dadyshkagoga.main()