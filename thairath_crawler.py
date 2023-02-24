import requests
import time
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple

from utils import clean


class ThairathCrawler:
    BASE_URL = 'https://www.thairath.co.th'
    NEWS_LIMIT = 10
    WAIT_TIME = 10

    def __init__(self, limit=NEWS_LIMIT, wait_time=WAIT_TIME):
        self.limit = limit
        self.wait_time = wait_time

    def fetch_news_data(self, timestamp: int, section: str = '/news/crime') -> Tuple[int, List[Dict]]:
        """Fetches news data from Thairath API"""
        response = requests.get(f'{self.BASE_URL}/loadmore', params={"section": section, "ts": timestamp, "limit": self.limit}).json()
        min_timestamp = response['minTs']
        news_items = response['items']
        return min_timestamp, news_items

    def fetch_news_content(self, news_id: str) -> Dict:
        """Fetches news content from Thairath API"""
        news_data = requests.get(f'{self.BASE_URL}/api-content/{news_id}').json()['items']
        return {
            "id": f"THR_{news_id}",
            "publish_date": news_data['publishTimeTh'],
            "source": 'ไทยรัฐ',
            "news_title": news_data['title'],
            "news_intro": news_data['abstract'],
            "news_description": clean(news_data['content']),
            "news_image": news_data['image']
        }

    def save_news_content(self, news_id: str, news_data: Dict) -> None:
        """Saves news content as a JSON file"""
        with open(f'data/THR_{news_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_data, json_file, ensure_ascii=False)

    def fetch_and_save_news(self) -> List[Dict]:
        """Fetches and saves Thairath news"""
        news_result = []
        timestamp = int(time.time() * 1000)

        while len(news_result) < self.limit:
            print(f"[THR] Loading News Before: {datetime.now()}")
            min_timestamp, news_items = self.fetch_news_data(timestamp)

            # Fetch news content and save it as a JSON file
            for item in news_items:
                print(f'[THR] Loading Thairath News Content {len(news_result) + 1}: {item["title"]}')
                id = item["id"]
                if not os.path.exists(f"data/THR_{id}.json"):
                    news_id = item['id']
                    news_data = self.fetch_news_content(news_id)
                    self.save_news_content(news_id, news_data)
                    news_result.append(news_data)
                else:
                    print(f'============ News THR_{id} is duplicate in the storage, find another news ============')
            timestamp = min_timestamp

        return news_result

    def run(self) -> None:
        """Runs the Thairath crawler indefinitely"""
        while True:
            print(f'============ Start Fetching Thairath News at {datetime.now()} ============')
            news = self.fetch_and_save_news()

            print(f'============ Finish Fetching Thairath News at {datetime.now()} ============')
            print(f'Waiting {self.wait_time} minutes to start fetching again')
            time.sleep(self.wait_time * 60)


if __name__ == '__main__':
    news_crawler = ThairathCrawler()
    news_crawler.run()
