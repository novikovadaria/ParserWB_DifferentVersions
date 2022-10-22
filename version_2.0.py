import requests
import json
import math

supplier = 18304


def get_json_all_info(url_to_products):
    product_info = []
    r = requests.get(url_to_products)
    data = r.json()
    for i in range(len(data['data']['products'])):
        product_info.append(supplier)
        id = data['data']['products'][i]['id']
        product_info.append(id)
        sizes_amount = len(data['data']['products'][i]['sizes'])
        for s in range(sizes_amount):
            sizes = data['data']['products'][i]['sizes'][s]['origName']
            product_info.append(sizes)
        inc_price = data['data']['products'][i]['salePriceU']
        price = int(inc_price/100)
        product_info.append(price)
        rating = data['data']['products'][i]['rating']
        product_info.append(rating)
        feedbacks = data['data']['products'][i]['feedbacks']
        product_info.append(feedbacks)
        print(product_info)


def count_page_amount(product_amount):
    page_amount = math.ceil(product_amount / 100)
    return page_amount


def get_json_total(url_to_amount):
    r = requests.get(url_to_amount)
    data = r.json()
    total = data['data']['total']
    product_amount = int(total)
    return product_amount


def main():
    supplier = 18304
    url_to_amount = f'https://catalog.wb.ru/sellers/filters?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-162903,-445299&emp=0&filters=xsubject&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=1&regions=80,68,64,83,4,38,33,70,82,69,86,75,30,40,48,1,22,66,31,71&spp=25&supplier={supplier}'
    product_amount = get_json_total(url_to_amount)
    page_amount = count_page_amount(product_amount)
    for q in range(1, page_amount+1):
        url_to_products = f'https://catalog.wb.ru/sellers/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-162903,-445299&emp=0&lang=ru&locale=ru&page={q}&pricemarginCoeff=1.0&reg=1&regions=80,68,64,83,4,38,33,70,82,69,86,75,30,40,48,1,22,66,31,71&sort=popular&spp=25&supplier={supplier}'
        get_json_all_info(url_to_products)


if __name__ == '__main__':
    main()
