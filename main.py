import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


API_URL = "https://api-ssl.bitly.com/v4"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    return parser


def api_request_url(url: str) -> str:
    url_parts = urlparse(url)
    return f"{API_URL}/bitlinks/{url_parts.netloc}{url_parts.path}"


def is_bitlink(token: str, url: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_request_url(url), headers=headers)
    return response.ok


def shorten_link(token: str, url: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "long_url": url,
        }
    response = requests.post(f'{API_URL}/shorten', headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token: str, url: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "units": "-1",
    }
    response = requests.get(f"{api_request_url(url)}/clicks/summary", headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def main():
    bitlink_token = os.getenv("BITLINK_ACCESS_TOKEN")
    parser = create_parser()
    line_args = parser.parse_args()
    try:
        # Making possible to use short url like "ya.ru"
        url_parsed = urlparse(line_args.url)
        url = f"http://{url_parsed.netloc}{url_parsed.path}"
        # Checking if url exist
        check_url = requests.get(url)
        check_url.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        exit("Ссылка не валидна".format(error))
    if is_bitlink(bitlink_token, url):
        try:
            clicks_count = count_clicks(bitlink_token, url)
        except requests.exceptions.HTTPError as error:
            exit("Не удалось получить количество кликов, проверьте токен".format(error))
        print(f"Количество кликов: {clicks_count}")
    else:
        try:
            bitlink = shorten_link(bitlink_token, url)
        except requests.exceptions.HTTPError as error:
            exit("Вы ввели неправильную ссылку, или ошибка в токене".format(error))
        print(f"Битлинк {bitlink}")


if __name__ == "__main__":
    load_dotenv()
    main()
