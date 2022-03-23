import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


BITLINK_TOKEN = os.getenv("BITLINK_ACCESS_TOKEN")
API_URL = "https://api-ssl.bitly.com/v4"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url')
    return parser


def base_bitlink_link(url: str) -> str:
    url_parts = urlparse(url)
    return f"{}/bitlinks/{url_parts.netloc}{url_parts.path}"


def is_bitlink(token: str, url: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(base_bitlink_link(url), headers=headers)
    return response.ok


def shorten_link(token: str, url: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    # Making possible to use short url_shorter like "ya.ru"
    url_parsed = urlparse(url)
    url = f"http://{url_parsed.netloc}{url_parsed.path}"
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
    response = requests.get(f"{base_bitlink_link(url)}/clicks/summary", headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def main():
    load_dotenv()
    parser = create_parser()
    line_args = parser.parse_args()
    if is_bitlink(BITLINK_TOKEN, line_args.url):
        try:
            clicks_count = count_clicks(BITLINK_TOKEN, line_args.url)
        except requests.exceptions.HTTPError as error:
            exit("Посчитать количество кликов не получилось".format(error))
        print(f"Количество кликов: {clicks_count}")
    else:
        try:
            bitlink = shorten_link(BITLINK_TOKEN, line_args.url)
        except requests.exceptions.HTTPError as error:
            exit("Ну что ты пихаешь, нужна нормальная ссылка".format(error))
        print(f"Битлинк {bitlink}")


if __name__ == "__main__":
    main()
