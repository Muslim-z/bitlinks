import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url,
        'units': -1
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
        headers=headers
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description='Введите ссылку для сокращения, или Битлинк для просмотра переходов по нему')
    parser.add_argument('url', help='Ваш URL')
    args = parser.parse_args()
    url = args.url
    parsed_url = urlparse(url)
    bitly_token = os.getenv('BITLY_TOKEN')
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'

    if is_bitlink(bitly_token, url_without_scheme):
        try:
            bitly_clicks_count = count_clicks(bitly_token, url_without_scheme)
            print(f'Количество переходов: {bitly_clicks_count}')

        except requests.exceptions.HTTPError:
            print('Не удалось посчитать кол-во кликов, опечатки в ссылке')

    else:
        try:
            print(f'Битлинк{shorten_link(bitly_token, url)}')

        except requests.exceptions.HTTPError:
            print('Ошибка при сокращении ссылки.')
