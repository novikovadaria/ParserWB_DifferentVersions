from bs4 import BeautifulSoup
from selenium import webdriver
import time


def end():
    for i in range(1, 4):
        file_path = f'C:/Users/79384/Desktop/WB парсер/page{i}.html'
        with open(file_path, encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        arts = soup.find_all('div', class_='product-card')
        list_art = []
        for art in arts:
            art_product = art.get('data-popup-nm-id')
            list_art.append(art_product)
        with open('article_numbers.txt', 'a', encoding="utf-8") as file:
            for art in list_art:
                file.write(f'{art}\n')
            print('all done')


def start():
    number_of_pages = int(input('Введите кол-во страниц: '))
    for i in range(1, number_of_pages+1):
        url = f'https://www.wildberries.ru/seller/700547?sort=popular&page={i}'
        driver = webdriver.Chrome()
        driver.get(url=url)
        time.sleep(5)
        with open(f'page{i}.html', 'w', encoding='UTF-8') as file:
            file.write(driver.page_source)
    driver.close()
    end()


start()