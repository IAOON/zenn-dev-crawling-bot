import os
from mastodon import Mastodon
from datetime import datetime

access_token = os.getenv('ACCESS_TOKEN')
api_base_url = os.getenv('API_BASE_URL')

mastodon = Mastodon(
    access_token = access_token,
    api_base_url = api_base_url
)

import requests
import json

def get_laftel_search_results():
    url = "https://laftel.net/api/search/v1/discover/?sort=recent&viewable=true&offset=0&size=60"
    response = requests.get(url)

    # 요청이 성공했는지 확인합니다.
    if response.status_code == 200:
        # 응답 내용을 'utf-8'로 디코딩하고 JSON으로 파싱합니다.
        data = json.loads(response.content.decode('utf-8'))
        return data
    else:
        print(f"Error occurred: {response.status_code}")

# 함수를 호출합니다.

try:
    data = get_laftel_search_results()
    count = data["count"]

    message = f"#라프텔 현재 라프텔에서 감상 가능한 작품은 {count} 개 있어요!"
    mastodon.toot(message)
except:
    message = "#라프텔 크롤링 중 에러가 발생했어요!"
    print(data)
    mastodon.toot(message)

