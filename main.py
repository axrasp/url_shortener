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


def generate_api_request_url(url: str) -> str:
    url_parts = urlparse(url)
    return f"{API_URL}/bitlinks/{url_parts.netloc}{url_parts.path}"


def is_bitlink(token: str, url: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(generate_api_request_url(url), headers=headers)
    return response.ok


def shorten_link(token: str, url: str, group_id: str, custom_domain: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "long_url": url,
        "group_guid": group_id,
        "domain": custom_domain,
    }
    response = requests.post(f'{API_URL}/shorten', headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token: str, url: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "units": "-1",
    }
    response = requests.get(f"{generate_api_request_url(url)}/clicks/summary", headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def main():
    bitlink_token = os.getenv("BITLINK_ACCESS_TOKEN")
    custom_domain = os.getenv("CUSTOM_DOMAIN")
    group_id = os.getenv("GROUP_ID")
    parser = create_parser()
    line_args = parser.parse_args()
    try:
        # Making possible to use short url like "ya.ru"
        url_parsed = urlparse(line_args.url)
        url = f"http://{url_parsed.netloc}{url_parsed.path}"
        # Checking if url exist
        response_url_check = requests.get(url)
        response_url_check.raise_for_status()
    except requests.exceptions.ConnectionError:
        exit("Ссылка не валидна")
    if is_bitlink(bitlink_token, url):
        try:
            clicks_count = count_clicks(bitlink_token, url)
        except requests.exceptions.HTTPError:
            exit("Не удалось получить количество кликов, проверьте токен")
        print(f"Количество кликов: {clicks_count}")
    else:
        try:
            bitlink = shorten_link(bitlink_token, url, group_id, custom_domain)
        except requests.exceptions.HTTPError:
            exit("Вы ввели неправильную ссылку, или ошибка в токене")
        print(f"Битлинк {bitlink}")


if __name__ == "__main__":
    load_dotenv()
    main()
