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
    headers = {
        'authority': 'laftel.net',
        'accept': 'application/json, text/plain, */*',
        'access_tokenept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_ga=GA1.1.1285760128.1681077693; ch-veil-id=64ce38fb-b3c8-41d5-9cb3-0c21b201aff1; colorScheme=dark; token="Token cefaeefa4e3249a1b1da50b183f76f4925ef3075"; user_id=136031; ab.storage.deviceId.76cc596b-05fd-4af0-aa6d-eccc8d54827f=%7B%22g%22%3A%22b8bd3f48-9f93-3ddd-e0e2-f18f47187070%22%2C%22c%22%3A1681077692405%2C%22l%22%3A1690160544688%7D; ab.storage.userId.76cc596b-05fd-4af0-aa6d-eccc8d54827f=%7B%22g%22%3A%222479545%22%2C%22c%22%3A1682056851907%2C%22l%22%3A1690160544688%7D; ab.storage.sessionId.76cc596b-05fd-4af0-aa6d-eccc8d54827f=%7B%22g%22%3A%227db87111-854e-787f-c5ca-767a5244f825%22%2C%22e%22%3A1690163346816%2C%22c%22%3A1690160544686%2C%22l%22%3A1690161546816%7D; ch_setting={"memberId":"p2479545","profile":{"defaultlafteluserid":136031,"name":"íœ´ë¦¬ìŠ¤í‹±","membershipType":"not_using","play":true}}; ch-session-7074=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI3MDc0LTYxNTkyN2YwNjEyMWU3ZGVlZTkyIiwiaWF0IjoxNjkwMTYxNTQ5LCJleHAiOjE2OTI3NTM1NDl9.NnY4tF38d3fn-Ozz-pFSZ-cNMFjNQhT19s0X9Jl30mU; _ga_900LJEBKB4=GS1.1.1690160546.52.1.1690161557.15.0.0',
        'laftel': 'TeJava',
        'referer': 'https://laftel.net/finder',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers = headers)

    # 요청이 성공했는지 확인합니다.
    if response.status_code == 200:
        # 응답 내용을 'utf-8'로 디코딩하고 JSON으로 파싱합니다.
        data = json.loads(response.content.decode('utf-8'))
        return data
    else:
        print(f"Error occurred: {response.status_code}")
        print(f"Error message: {response.text}")

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

