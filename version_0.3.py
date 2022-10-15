from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

#Загрузка кода страницы после того, как документ загрузится
def http_page_fullloaded_to_text(url):
    # <----- Открываем ссылку, ждем пока страница полностью загрузится, забираем html код
    driver = webdriver.Chrome()
    driver.get(url=url)
    # Ждем секунду, а потом если не хватило до тех пор, пока не загрузится страница
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    return driver.page_source

def page_fullloaded_to_text(url):
    # <----- Открываем продавца на первой стр, забираем html код
    driver = webdriver.Chrome()
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

def find_wb_pages_amount(http_code):
    soup = BeautifulSoup(http_code, 'lxml')
    element = soup.find('div', class_='seller-details__count-products')
    article_amount = int(element.find('span').text)
    return math.ceil(article_amount / 100)

def main():
    seller_id = 700547
    seller_url = 'https://www.wildberries.ru/seller/' + str(seller_id) + '?sort=popular'
    http_code = page_fullloaded_to_text(seller_url + '&page=1')
    pages_amount = find_wb_pages_amount(http_code)
    art_list = []
    art_list = find_wb_articles(http_code)

    # <----- В цикле достаём все остальные страницы с товаром и дописываем артикулы в общий список артикулов
    for i in range(2, pages_amount+1):
        http_code = page_fullloaded_to_text(seller_url + f'&page={i}')
        art_list.extend(find_wb_articles(http_code))

    # <----- Записываем найденные артикулы в файл
    with open('article_numbers.txt', 'a', encoding="utf-8") as file:
        for art in art_list:
            file.write(f'{art}\n')
        print('all done')

if __name__ == '__main__':
    main()
