import requests

from products.models import Product
from products.scrap_settings import (categories_ids, categories_revers,
                                     cookies, headers)

"""
{
    'name': 'Смартфон Apple iPhone 11 64GB White',
    'price_now': '35 999',
    'price_old': '57 999',
    'quantity': '10',
    'specifications': '?',
    'image1': 'https://img.mvideo.ru/Big/30063493bb.jpg',
    'image2': 'https://img.mvideo.ru/Big/30063493bb1.jpg',
    'image3': 'https://img.mvideo.ru/Big/30063493bb2.jpg',
    'category': 'Смартфоны',
    'short_description': 'Берите выше. iPhone 11. Система двух камер со сверхширокоугольной камерой.
                        Ночной режим и потрясающее качество видео. Защита от воды и пыли.
                         Длительная работа без подзарядки. Шесть прекрасных цветов. 11 станет вашим
                         любимым числом. Характеристики • ЖК‑дисплей Liquid Retina HD 6,1 дюйма • Защита
                         от воды и пыли (при погружении на глубину до 2 метров длительностью до 30 минут (IP68)) •',
    'description':  'Берите выше. iPhone 11. Система двух камер со сверхширокоугольной камерой.....'
    'colors': ['желтый','синий']
}

"""


def scraping():
    for cat_id in categories_revers:
        params = {
            'categoryId': cat_id,
            'offset': '0',
            'limit': '24',
            'filterParams': [
                'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ',
            ],
            'doTranslit': 'true',
        }
        response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                                headers=headers).json()
        pages = int(response['body']['total'])
        id_list = response['body']['products']
        for i in range(23, pages, 23):
            params['offset'] = i
            response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                                    headers=headers).json()
            if len(id_list) >= 50:
                break
            for j in (response['body']['products']):
                if j not in id_list:
                    id_list.append(j)
                if len(id_list) >= 25:
                    break
        for id in id_list:
            try:
                response = requests.get(f'https://www.mvideo.ru/bff/product-details?productId={id}&multioffer=true',
                                        cookies=cookies, headers=headers).json()
                response_price = requests.get(f'https://www.mvideo.ru/bff/products/prices?productIds={id}'
                                              f'&isPromoApplied=true&addBonusRubles=true',
                                              cookies=cookies, headers=headers).json()
                specif = list()
                for i in response['body']['properties']['key']:
                    for j in i['properties']:
                        specif.append(
                            f"{j['name']}: {j['value']}.{j['nameDescription'] if j['nameDescription'] else ''}")
                if response['body']['variants']:
                    colors = list()
                    for color in response['body']['variants'][0]:
                        if color['attributeId'] == 89:
                            for val in color['values']:
                                colors.append(val['value'])
                else:
                    colors = list()
                img3 = f"https://img.mvideo.ru/{response['body']['images'][3]}" if len(
                    response['body']['images']) > 3 else " "
                price_discount = response_price['body']['materialPrices'][0]['price']['basePromoPrice']
                item = {
                    'name': response['body']['name'],
                    'price_now': price_discount if price_discount else
                    response_price['body']['materialPrices'][0]['price']['basePrice'],
                    'price_old': response_price['body']['materialPrices'][0]['price']['basePrice'],
                    'quantity': 10,
                    'specifications': specif,
                    'image1': f"https://img.mvideo.ru/{response['body']['images'][1]}" if response['body']['images'][
                        1] else None,
                    'image2': f"https://img.mvideo.ru/{response['body']['images'][2]}" if response['body']['images'][
                        2] else None,
                    'image3': img3,
                    'category': categories_revers[params['categoryId']],
                    'short_description': response['body']['description'],
                    'description': response['body']['description'],
                    'colors': colors,
                    'slug': response['body']['nameTranslit'],
                    'brand': response['body']['brandName'],
                }
            except Exception as exc:
                print(exc)
                continue

            disc = round(100 - item['price_now'] / item['price_old'] * 100)
            if disc == 0:
                disc = None

            nwords = ['Black', 'Green', '128GB', '4/128Gb', '256GB', 'Space', 'Light', 'Dark Green',
                      'Light Silver', 'White', 'Sierra Blue', 'Midnight', 'Alpine Green', 'Blue', 'Gray',
                      'Quantum Black',
                      'Purple', 'Dawn Gold', 'Granite Gray', 'Silver', 'Dark']
            result_name = list()
            for name in item['name'].split():
                for n in nwords:
                    if name == n:
                        break
                else:
                    result_name.append(name)
            if not Product.objects.filter(name=" ".join(result_name)).exists():
                Product.objects.create(
                    name=" ".join(result_name),
                    price_now=item['price_now'],
                    price_old=item['price_old'],
                    quantity=item['quantity'],
                    specifications="\n".join(item['specifications']),
                    image1=item['image1'],
                    image2=item['image2'],
                    image3=item['image3'],
                    category_id=categories_ids[categories_revers[cat_id]],
                    short_description=item['short_description'],
                    description=item['description'],
                    colors=",".join(item['colors']).title(),
                    slug=item['slug'],
                    discount=disc,
                    brand=item['brand']
                )
            print(item['brand'])


if __name__ == '__main__':
    scraping()
