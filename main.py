#-*- coding: utf-8 -*-

import os
from mastodon import Mastodon
from datetime import datetime

access_token = os.getenv('MASTODON_ACCESS_TOKEN')
api_base_url = os.getenv('API_BASE_URL')
zenn_dev_base_url = os.getenv('ZENN_DEV_BASE_URL')

mastodon = Mastodon(
    access_token = access_token,
    api_base_url = api_base_url
)
import requests
from bs4 import BeautifulSoup

def crawling():
    url = "https://zenn.dev"
    response = requests.get(url)

    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'lxml')

    base_selector = 'html > body > div:nth-of-type(1) > section:nth-of-type(1) > div > div:nth-of-type(2) > div > div:nth-of-type(1)'
    additional_selector = 'article > div > a'

    # 기본 CSS selector를 가진 첫번째 요소를 선택
    base_element = soup.select_one(base_selector)

    if base_element is not None:
        # 기본 요소 내부에서 추가적인 요소를 선택
        additional_element = base_element.select_one(additional_selector)

        # 선택된 요소들의 텍스트를 출력
        print("Base element text: ", base_element.text)
        if additional_element is not None:
            data = {"title": additional_element.text, "link": additional_element.get('href')}
            return data;
            # print("Additional element text: ", additional_element.text)
            # 요소의 href 값을 출력
            # print("Additional element href: ", additional_element.get('href'))
        else:
            print("No additional element found within the base element.")
    else:
        print("No base element found.")
    
try:
    data = crawling()

    message = f"""
    Trend Post
    Title : {data["title"]}
    Link : {zenn_dev_base_url[:-1]}/{data["link"][1:]}
    """
    
    mastodon.toot(message)
except Exception as e:
    print(f"An exception occurred: {e}")
    mastodon.toot(message)

