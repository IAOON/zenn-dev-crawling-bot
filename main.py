# !pip3 install feedparser
# !pip3 install pandas
#-*- coding: utf-8 -*-

import os
import json
from urllib import parse
import urllib.request
from mastodon import Mastodon
from datetime import timedelta, datetime
from dateutil import parser
import requests
import feedparser

access_token = os.getenv('MASTODON_ACCESS_TOKEN')
api_base_url = os.getenv('API_BASE_URL')
zenn_dev_base_url = os.getenv('ZENN_DEV_BASE_URL')

NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

mastodon = Mastodon(
    access_token = access_token,
    api_base_url = api_base_url
)

import requests
import pandas as pd
import random

# 데이터프레임을 csv 파일로 저장하는 함수
def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def add_translation_reply(reply_to, entry):
    original_url = entry['link']
    original_text = entry['title']

    for locale in ["en", "ko"]:
        data = f"source=ja&target={locale}&text={original_text}"
        papago_url = f"https://papago.naver.net/website?locale=ko&source=ja&target={locale}&url={parse.quote(original_url)}"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        status_code = response.getcode()
        if(status_code == 200):
            response_body = response.read()
            response_body_decoded = response_body.decode('utf-8')
            result = json.loads(response_body_decoded)['message']['result']['translatedText']

            message = f"""Trend Post\nTitle : {result}\nLink : {papago_url}"""
            mastodon.status_reply(reply_to, message, language=locale)
        else:
            print("Error Code:" + status_code)

# csv 파일을 읽어와서 데이터를 DataFrame으로 반환하는 함수
def read_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        # 데이터프레임이 비어있는지 확인
        if df.empty:
            return []
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        return []
    return df

def feed_crawling():
    FEED_URL = 'https://zenn.dev/feed'
    rss_feed = feedparser.parse(FEED_URL)

    used_items = read_from_csv("used_item.csv")

    for entry in rss_feed.entries:
        object = {"title":entry.title, "link": entry.links[0].href}

        if (object not in used_items):
            data.append(object)

    if (data == []):
        return # 모두 중복이면 포스팅할 것 없음

    print_entry = random.choice(data)

    message = f"""Trend Post\nTitle : {print_entry["title"]}\nLink : {print_entry["link"]}"""
    reply_to = mastodon.status_post(message, language = "ja")

    add_translation_reply(reply_to, print_entry)
    used_items.append({"title":print_entry["title"], "link":{print_entry["link"]}})

    export_to_csv(used_items, "used_item.csv")

feed_crawling()
