from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math


def main():
    # <----- Открываем продавца на первой стр, забираем html код
    url = 'https://www.wildberries.ru/seller/700547?sort=popular&page=1'
    driver = webdriver.Chrome()
    driver.get(url=url)
    time.sleep(3.5)
    with open(f'page1.html', 'w', encoding='UTF-8') as file:
        file.write(driver.page_source)
    driver.close()

    # <----- Находим кол-во страниц, найдя общее число товара, разделив на 100 и округлив
    with open('page1.html', encoding='UTF-8') as file:
        source = file.read()
    soup = BeautifulSoup(source, 'lxml')
    element = soup.find('div', class_='seller-details__count-products')
    amount = element.find('span').text
    int_am = int(amount)
    pages = math.ceil(int_am/100)

    # <----- В цикле достаём все остальные страницы с товаром
    for i in range(2, pages+1):
        url = f'https://www.wildberries.ru/seller/700547?sort=popular&page={i}'
        driver = webdriver.Chrome()
        driver.get(url=url)
        time.sleep(5)
        with open(f'page{i}.html', 'w', encoding='UTF-8') as file:
            file.write(driver.page_source)
    driver.close()

    # <----- Находим артикулы
    for i in range(1, pages+1):
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


if __name__ == '__main__':
    main()
