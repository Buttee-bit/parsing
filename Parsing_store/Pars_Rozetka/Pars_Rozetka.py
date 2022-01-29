from bs4 import BeautifulSoup
import requests
import csv





def request(url,config):
    r = requests.get(url,headers=config)
    if r.status_code == 200:
        return r.text
    else:
        print('Ошибка подключения')


def config():
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    return headers

def main():
    headers = config()
    url = "https://rozetka.com.ua/ua/"
    request(url,headers)

main()