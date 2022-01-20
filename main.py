import os
from dotenv import load_dotenv
import requests


def shorten_link(token, url):
    parara = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=parara,
        json=payload
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    parara = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=parara
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    parara = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
        headers=parara
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    url = input()
    token = os.getenv('TOKEN')
    if is_bitlink(token, url):
        try:
            print(count_clicks(token, url))
        except requests.exceptions.HTTPError:
            print("неудалось посчитать кол-во кликов, опечатки в ссылке")
    else:
        try:
            print('Битлинк ' + shorten_link(token, url))

        except requests.exceptions.HTTPError:
            print("ошибка при сокращении ссылки.")
