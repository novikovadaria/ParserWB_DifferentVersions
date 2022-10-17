# ИНСТРУКЦИЯ
# Перед запуском убедитесь в правильных настройках подключения к Вашей БД и правильном пути к файлу Лога

import math
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
import pymysql.cursors

seller_id = '700547'  # номер магазина WB, по которому работает парсер
logfile = open('wb_parser_log.txt', 'a')  # Локальный лог
# logfile = open('/usr/myScripts/wbparser/wb_parser_log.txt', 'a') #Серверный лог
cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Запуск драйвера и браузера Chrome
def chrome_driver_init():
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

# Создание подключения к БД


def DB_connection_init():

    # Данные для подключения к БД
    db_host = 'localhost'
    db_port = 3306
    db_user = 'root'
    db_password = '24465336Kotiki'
    db_name = 'testing_db'
    db_charset = 'utf8'
    seller_id = '700547'

    connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                 charset=db_charset, cursorclass=pymysql.cursors.DictCursor)
    return connection

# Загрузка кода страницы, открытой через браузер, после того, как она вся прогрузится


def page_fullloaded_to_text(driver, url):
    # <----- Открываем продавца на первой стр, забираем html код
    driver.get(url=url)
    # Ждем секунду, а потом если не хватило до тех пор, пока не загрузится страница
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    return driver.page_source

# Формирование списка артикулов на странице из ее html-кода


def find_wb_articles(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    arts = soup.find_all('div', class_='product-card')
    art_list = []
    for art in arts:
        art_product = art.get('data-popup-nm-id')
        art_list.append(art_product)
    return art_list

# Формирование списка цен на странице из ее html-кода


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

# Расчет количества страниц товаров в магазине


def find_wb_pages_amount(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    element = soup.find('div', class_='seller-details__count-products')
    article_amount = int(element.find('span').text)
    logwrite('dop_info', 'Количество товаров в магазине: ' + str(article_amount))
    return math.ceil(article_amount / 100)

# Добавление найденных артикулов WB в БД


def art_to_db(art_list, price_list):
    # <---- Подключаемся к базе данных (должна быть создана предварительно)
    connection = DB_connection_init()

    # Подготавливаем запрос на добавление всех найденных артикулов
    with connection.cursor() as cursor:
        if len(art_list) == len(price_list):
            for i in range(len(art_list)):
                cursor.execute(
                    f"INSERT INTO `testing_db`.`history_wb` (`shop_id`, `article_wb`, `price`, `time_of_session`) VALUES ('{seller_id}', '{art_list[i]}','{price_list[i]}', '{datetime.now()}');")
        else:
            logfile.write('Количество артикул и цен несовпадает.\n')

    # Выполняем запрос
    connection.commit()
    connection.close()

# Формирование строки со статусом ОК с выравниванием по правому краю


def end_current_OK(message_text):
    total_string_OK_length = 70
    result = ''
    for i in range(1, total_string_OK_length - len(message_text)-2):
        result += '.'
    result += 'OK'
    return result

# Добавить запись в лог


def logwrite(arg, message_text=''):
    if arg == 'step_begin' or arg == 'exception':
        print(message_text, end='')
        logfile.write(cur_time + ' ' + message_text)
    if arg == 'step_OK':
        print(end_current_OK(message_text))
        logfile.write(end_current_OK(message_text) + '\n')
    if arg == 'dop_info':
        print(message_text)
        logfile.write(cur_time + ' ' + message_text + '\n')
    if arg == 'empty':
        logfile.write('\n')

# Основная программа


def main():
    message_text = 'Запускаем браузер'
    logwrite('step_begin', message_text)
    driver = chrome_driver_init()  # Запускаем браузер Chrome
    logwrite('step_OK', message_text)

    try:
        # Формируем ссылку на магащин
        seller_url = f'https://www.wildberries.ru/seller/{seller_id}?sort=popular'
        message_text = 'Загружаем страницу 1'
        logwrite('step_begin', message_text)

        # Скачиваем код первой страницы после того, как она прогрузится
        http_code = page_fullloaded_to_text(driver, seller_url + '&page=1')
        logwrite('step_OK', message_text)

        # Определяем сколько страниц товаов в магазине
        pages_amount = find_wb_pages_amount(http_code)
        # Находим на первой странице все артикулы товаров
        art_list = find_wb_articles(http_code)
        # Находим на первой странице все цены товаров
        price_list = find_wb_price(http_code)

        logwrite(
            'dop_info', 'Количество страниц товаров в магазине: ' + str(pages_amount))

        # <----- В цикле достаём все остальные страницы с товаром и дописываем артикулы в общий список артикулов
        for i in range(2, pages_amount+1):  # Для каждой страницы товаров
            message_text = f'Загружаем страницу {i}'
            logwrite('step_begin', message_text)

            http_code = page_fullloaded_to_text(
                driver, seller_url + f'&page={i}')  # Скачиваем код i-й страницы
            # Находим на i-й странице все артикулы товаров
            art_list.extend(find_wb_articles(http_code))
            # Находим на i-й странице все цены товаров
            price_list.extend(find_wb_price(http_code))

            logwrite('step_OK', message_text)

        message_text = f'Загружаем все артикулы и цены в базу данных'
        logwrite('step_begin', message_text)

        art_to_db(art_list, price_list)  # записываем артикулы в БД

        logwrite('step_OK', message_text)

    except Exception as err:
        logwrite('exception', "\n" + "Возникла ошибка: " + str(err.args) + "\n")
    finally:
        logwrite('empty', '')
        driver.close()  # Закрытие браузера
        logfile.close()


if __name__ == '__main__':
    main()
