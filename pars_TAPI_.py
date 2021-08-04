import json  # Что б сохранять значения в формате json
import time  # Что б задавать время (сна)
import csv  # Что б сохранять
import random  # Что б задавать рандомное значение сна
from random import choice
from bs4 import BeautifulSoup  # Библиотека BS для логики сбора информации
import requests  # Библиотека requests что бы обращаться к сайтам
from fake_useragent import UserAgent  # fake_useragent для 'обмана сайта'

# Импортируем необходимые библиотеки

class Tapki_Spyder:  # Создаем класс парсера (Потому что могу в классах)

    def __init__(self, name, link):  # Конструктор класса , каждый объек будет иметь ИМЯ и ССЫЛКУ
        self.name = name
        self.link = link
        print(f'Создан паук с именем <<{self.name}>>, занимающийся скрпаингом сайта {self.link}')

    def get_proxy(self):
        list_proxy = open('Proxylist.txt').read().split('\n')
        proxy = {'http': 'http://' + choice(list_proxy)}
        return proxy

    def get_response(self, i, match):  #  Метод принимает на вход счетчик и количество итераций
        print(f'Открываем {i} протокол')  # Графическая составляющая
        try:
            r = requests.get((self.link + str(i)), headers={'User-Agent': UserAgent().chrome})  #  Получаем положительный ответ от сервера (responce 200)
            time.sleep(random.randint(5, 8))  # Время , что б сайт не принял нас за бота
            print(f'Отлично, готово {i + 1} из {match}')  # Графическая составляющая (У нас тут как бы еще ничего не готово , но это не имеет значения ))))))
            print(f'Работа готова на {round(((i + 1) / match) * 100, 2)}%')  # Графическая составляющая показывающая в процентах на сколько готово "завершение программы"
            page = r.text  # получаем сам код со страницы
            self.save_page_html(page, i)  # Вызываем метод для сохранения нашего кода страницы в отдельный файл
        except requests.exceptions.ConnectionError:
            a = 'Сайт нас забанил !'
            print(a)
            return True


    def save_page_html(self, page, i):  # Метод принимающий сам код страницы и счетчик (номер нашего протокола)
        with open(f'data_ports_HTML/page_ports{i}.html', 'w', encoding='utf-8') as file:  # Открываем файл на запись
            file.write(page)  # Записываем код страницы в файл (HTML)

    def open_page(self, path):  # Функция  открытия HTML файла для дальнейшей работы с ним
        with open(path, 'r', encoding='utf-8') as file:  # Открывем файл на чтение
            data = file.read()  # Читаем весь файл
            return data  # Возвращаем наш прочитанный файл

    def get_content(self, path):  # Функция , котрая принимает в аргументы адресс  записанного HTML файла
        data = self.open_page(path)  # Вызываем функцию открывающую HTML
        soup = BeautifulSoup(data, 'lxml')  # Создаем объект СУП
        data_to_port = soup.find_all('table')[2].find_all('tr')  # Ищем по структуре страницы необходимый нам блок[Получаем список]
        data = []  # Список в котром у нас будут храниться интересующие нас данные
        for info in data_to_port:  # Пока элемент есть в списке
            try:  # Обработка исключений
                port = info.find_all('td')[0].text  # Находим блок с информацией о порте
                protocol = info.find_all('td')[1].text  # Находим блок с информацией о протоколе
                service = info.find_all('td')[2].text  # Находим блок с информацией о серфисе
                details = info.find_all('td')[3].text  # Находим блок с информацией о деталях
                source = info.find_all('td')[4].text  # Находим блок с информацией о источниках
                data.append({
                    'port': port,
                    'protocol': protocol,
                    'service': service,
                    'details': details,
                    'source': source
                })  # В список добавляем словари
            except:  # Обработка исключений
                pass  # Если найдено исключение , то ничего не делаем
        return data  # Возвращаем наш список словарей

    def save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def save_csv(self, path, data):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['port', 'protocol', 'service', 'details', 'source'])
            for item in data:
                writer.writerow([item['port'], item['protocol'], item['service'], item['details'], item['source'], ])

    def main(self):  # main не много не мэйн , по хорошему переписать бы строки с циклом в отдельный 'метод'
        print('Всего протоколов: 65535')
        match = int(input('Введите количество протоколов информацию о которых хотите узнать\n'))  # Задаем количесвто протоколов , которые хотим собрать
        data = []  # Контейнер, в котором будем хранить словари (список словарей )
        counter = 0  # Просто счетчик , при помощи которого будет удобно делать (визуализацию работы программы)
        for i in range(match):  # Цикл для того что бы пройти о всем ссылка + собрать информацию
            Flag = self.get_response(i, match)  # Получаем страниу с которой собираем информацию
            if Flag == True:
                break
            data += self.get_content(f"data_ports_HTML\page_ports{i}.html")  # Добавляем в список полученную информацию
            counter += 1  # Увеличиваем счетчик(Счетчик принимает ровно теже значения , что и {i}, но так удобно)

        self.save_json(data, f'data_ports_JSON/data.json')  # Полученнй список словарей записываем в формате json (мб лучше записывать каждую страницу отдельно ?)
        self.save_csv(f'data_ports_CSV/data.csv', data)  # Полученный список словарей записываем в формате csv (ЭКСЕЛЬ) вот тут точно нужно ВСЕ данные по итогу записать


name = 'Поставьте 5 по алгоритмам, ПОЖАЛйЙСТА'  # Имя нашего парсера

link = 'https://www.speedguide.net/port.php?port=0'  # Первая страница , с которой будет работать наш парсер

spyder = Tapki_Spyder(name, link)  # Создаем объек класса "Tapki_Spyder" со своим именем и страницей
spyder.main()  # Вызываем метод main (основная функция, которая во время исполнения будет делать необходимые действия)
