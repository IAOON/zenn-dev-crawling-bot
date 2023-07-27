#-*- coding: utf-8 -*-

import os
from mastodon import Mastodon
from datetime import timedelta, datetime
from dateutil import parser
import requests
import feedparser

access_token = os.getenv('MASTODON_ACCESS_TOKEN')
api_base_url = os.getenv('API_BASE_URL')
zenn_dev_base_url = os.getenv('ZENN_DEV_BASE_URL')

mastodon = Mastodon(
    access_token = access_token,
    api_base_url = api_base_url
)

import requests

def feed_crawling():
    FEED_URL = 'https://zenn.dev/feed' 

    rss_feed = feedparser.parse(FEED_URL)

    for entry in rss_feed.entries:
        parsed_date = parser.parse(entry.published)
        parsed_date = parsed_date.replace(tzinfo=None)
        now_date = datetime.utcnow()

        published_30_minutes_ago = (now_date - parsed_date) < timedelta(minutes=1000)
        if published_30_minutes_ago:
            message = f"""
                Trend Post
                Title : {entry.title}
                Link : {entry.links[0].href}
            """
            # print(message)
            mastodon.toot(message)

feed_crawling()
