import requests
import math
import pymysql
import pymysql.cursors
from datetime import datetime

supplier = 18304
logfile = open('wb_parser_log.txt', 'a')  # Локальный лог
cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
products = []


def DB_connection_init():
    message_text = 'Подключение к базе данных'
    logwrite('step_begin', message_text)

    # # Данные для подключения к БД Новикова Дарья
    db_host = 'localhost'
    db_port = 3306
    db_user = 'root'
    db_password = '24465336Kotiki'
    db_name = 'testing_db'
    db_charset = 'utf8'

    # Установление соединения
    connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                 charset=db_charset, cursorclass=pymysql.cursors.DictCursor)

    logwrite('step_OK', message_text)

    return connection

# Формирование массива с информацией по товарам на указанной странице указанного поставщика


def get_json_all_info(supplier, page):
    message_text = f'Загрузка инфо о товарах со страницы {page}'
    logwrite('step_begin', message_text)

    url_to_products = f'https://catalog.wb.ru/sellers/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-162903,-445299&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&reg=1&regions=80,68,64,83,4,38,33,70,82,69,86,75,30,40,48,1,22,66,31,71&sort=popular&spp=25&supplier={supplier}'
    r = requests.get(url_to_products)
    data = r.json()
    product_count = len(data['data']['products'])
    for i in range(product_count):
        id = data['data']['products'][i]['id']
        sizes_amount = len(data['data']['products'][i]['sizes'])
        price = int(data['data']['products'][i]['salePriceU'] / 100)
        rating = data['data']['products'][i]['rating']
        feedbacks = data['data']['products'][i]['feedbacks']
        for j in range(sizes_amount):
            product_info = []
            size = data['data']['products'][i]['sizes'][j]['origName']
            product_info.append(supplier)
            product_info.append(id)
            product_info.append(size)
            product_info.append(price)
            product_info.append(rating)
            product_info.append(feedbacks)
            products.append(product_info)

    logwrite('step_OK', message_text)
    logwrite('dop_info', 'Количество товаров найдено: ' + str(product_count))

# Получение количества всех страниц товаров поставщика


def get_json_pages_total(supplier):
    message_text = f'Расчет количества страниц товаров'
    logwrite('step_begin', message_text)

    url_to_amount = f'https://catalog.wb.ru/sellers/filters?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-162903,-445299&emp=0&filters=xsubject&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=1&regions=80,68,64,83,4,38,33,70,82,69,86,75,30,40,48,1,22,66,31,71&spp=25&supplier={supplier}'
    r = requests.get(url_to_amount)
    data = r.json()
    total = data['data']['total']
    product_amount = int(total)
    page_amount = math.ceil(product_amount / 100)

    logwrite('step_OK', message_text)
    logwrite('dop_info', 'Количество товаров найдено: ' + str(product_amount))
    logwrite('dop_info', 'Количество страниц: ' + str(page_amount))

    return page_amount

# Загрузка всех товаров в БД


def info_to_db(connection, products):
    message_text = f'Загрузка данных по товарам в БД'
    logwrite('step_begin', message_text)

    insert_string = 'INSERT INTO `db_json`.`history_wb` (`shop_id`, `article_wb`, `size`, `price`, `rating_stars`, `feedbacks_count`, `time_of_session`) VALUES '
    # Заполнение значениями запроса
    for product in products:
        insert_string += f"('{product[0]}', '{product[1]}', '{product[2]}', '{product[3]}', '{product[4]}', '{product[5]}', '{cur_time}'), "
    # Удаление последней запятой
    insert_string = insert_string[0:(len(insert_string)-2)]

    # Выполнение запроса
    with connection.cursor() as cursor:
        cursor.execute(insert_string)

    logwrite('step_OK', message_text)
    logwrite('dop_info', 'Количество загруженных товаров: ' + str(len(products)))

# Загрузка данных о номерах магазинах, по которым нужно провести парсинг


def get_suppliers(connection):
    message_text = f'Загрузка кодов магазинов для парсинга из БД'
    logwrite('step_begin', message_text)

    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT `wb_parser_suppliers`.`supplier_num` FROM `db_json`.`wb_parser_suppliers`;")
    connection.commit()
    response = cursor.fetchall()
    suppliers = []
    for row in response:
        suppliers.append(row['supplier_num'])

    logwrite('step_OK', message_text)

    return suppliers

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
        print()
        logfile.write('\n')


def main():
    try:
        # Считывание списка магазинов для обработки
        connection = DB_connection_init()
        suppliers = get_suppliers(connection)
        for supplier in suppliers:
            logwrite('empty', '')
            logwrite(
                'dop_info', f'Обработка данных товаров магазина {supplier}')

            products.clear()
            # Вычисление количества страниц товаров у указанного поставщика
            page_amount = get_json_pages_total(supplier)

            # Добавление в общий список товаров с каждой страницы поставщика
            for page in range(1, page_amount+1):
                get_json_all_info(supplier, page)

            # Загрузка всей информацию по каждому товару в базу данных
            info_to_db(connection, products)
    except Exception as err:
        logwrite('exception', "\n" + "Возникла ошибка: " + str(err.args) + "\n")
    finally:
        if logfile.closed == False:
            logwrite('empty', '')
            logfile.close()
            connection.close()


if __name__ == '__main__':
    main()
