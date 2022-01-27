import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests


def shorten_link(token, url):
    params = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=params,
        json=payload
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    params = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=params
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    params = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
        headers=params
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    print(
        'Введите ссылку для сокращения, или Битлинк для просмотра переходов по нему'
    )
    url = input('Ваша ссылка или Битлинк: ')
    parsed_url = urlparse(url)
    token = os.getenv('TOKEN')
    if is_bitlink(token, parsed_url.netloc + parsed_url.path):
        try:
            print(f'Количество переходов: {count_clicks(token, parsed_url.netloc + parsed_url.path)}')
        except requests.exceptions.HTTPError:
            print('Неудалось посчитать кол-во кликов, опечатки в ссылке')
    else:
        try:
            print('Битлинк ' + shorten_link(token, url))

        except requests.exceptions.HTTPError:
            print('Ошибка при сокращении ссылки.')
