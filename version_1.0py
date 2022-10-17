import math
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
import pymysql.cursors


db_host = 'localhost'
db_port = 3306
db_user = 'root'
db_password = '24465336Kotiki'
db_name = 'testing_db'
db_charset = 'utf8'
seller_id = '700547'


def http_page_fullloaded_to_text(url):
    # <----- Открываем ссылку, ждем пока страница полностью загрузится, забираем html код
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)
    # Ждем секунду, а потом если не хватило до тех пор, пока не загрузится страница
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    return driver.page_source


def page_fullloaded_to_text(url):
    # <----- Открываем продавца на первой стр, забираем html код
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)
    # Ждем секунду, а потом если не хватило до тех пор, пока не загрузится страница
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    return driver.page_source


def find_wb_articles(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    arts = soup.find_all('div', class_='product-card')
    art_list = []
    for art in arts:
        art_product = art.get('data-popup-nm-id')
        art_list.append(art_product)

    return art_list


def find_wb_price(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    blocks = soup.find_all('span', class_='price')
    price_list = []
    for card in blocks:
        str_price = card.find('ins', class_='lower-price').text
        correct_form_price = str_price.replace('                ', '').replace(
            '₽', '').replace('            ', '').replace('\xa0', '')
        price = int(correct_form_price)
        price_list.append(price)

    return price_list


def find_wb_pages_amount(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    element = soup.find('div', class_='seller-details__count-products')
    article_amount = int(element.find('span').text)
    return math.ceil(article_amount / 100)

# Добавление найденных артикулов WB в БД


def data_to_db(art_list, price_list):
    # <---- Подключаемся к базе данных (должна быть создана предварительно)
    connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                 charset=db_charset, cursorclass=pymysql.cursors.DictCursor)
    # Подготавливаем запрос на добавление всех найденных артикулов
    with connection.cursor() as cursor:
        if len(art_list) == len(price_list):
            for i in range(len(art_list)):
                cursor.execute(
                    f"INSERT INTO `testing_db`.`history_wb` (`shop_id`, `article_wb`, `price`, `time_of_session`) VALUES ('{seller_id}', '{art_list[i]}','{price_list[i]}', '{datetime.now()}');")
        else:
            pass

    # Выполняем запрос
    connection.commit()
    connection.close()


def main():
    seller_url = f'https://www.wildberries.ru/seller/{seller_id}?sort=popular'
    print('Загружаем страницу 1')
    http_code = page_fullloaded_to_text(seller_url + '&page=1')
    pages_amount = find_wb_pages_amount(http_code)
    art_list = find_wb_articles(http_code)
    price_list = find_wb_price(http_code)

    # <----- В цикле достаём все остальные страницы с товаром и дописываем артикулы в общий список артикулов
    for i in range(2, pages_amount+1):
        print(f'Загружаем страницу {i}')
        http_code = page_fullloaded_to_text(seller_url + f'&page={i}')
        art_list.extend(find_wb_articles(http_code))
        price_list.extend(find_wb_price(http_code))

    print(f'Загружаем все артикулы в базу данных')
    data_to_db(art_list, price_list)


if __name__ == '__main__':
    main()
