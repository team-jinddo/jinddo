import scrapy
import json
import pandas as pd
import os

class ReviewSpider(scrapy.Spider):
    name = "reviews_spider" # 파일명
    
    # 수집할 데이터를 초기화합니다.
    custom_settings = {
    # Limit the concurrent requests to reduce load and avoid being blocked
    'CONCURRENT_REQUESTS': 8,  # Start with 8 concurrent requests and adjust if necessary
    'CONCURRENT_REQUESTS_PER_DOMAIN': 4,  # Limit concurrent requests to the same domain

    # Introduce a delay between requests to avoid rapid request bursts
    'DOWNLOAD_DELAY': 0.5,  # Set a delay of 0.5 seconds between requests
    'RANDOMIZE_DOWNLOAD_DELAY': True,  # Randomize delay to prevent a predictable pattern

    # Enable AutoThrottle to dynamically adjust the download delay based on server response times
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 1,  # Initial delay set for AutoThrottle
    'AUTOTHROTTLE_MAX_DELAY': 3,  # Maximum delay to be applied when server load is high
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # Target concurrency: average of 1 request at a time
    'AUTOTHROTTLE_DEBUG': False,  # Set to True to see throttling information in the logs

    # Retry settings to handle failed requests gracefully
    'RETRY_ENABLED': True,
    'RETRY_TIMES': 3,  # Retry failed requests up to 3 times before giving up

    # Enable HTTP caching to avoid redundant downloads and reduce load on the server
    'HTTPCACHE_ENABLED': True,
    'HTTPCACHE_EXPIRATION_SECS': 3600,  # Cache expiration time (1 hour)
    'HTTPCACHE_DIR': 'httpcache',
    'HTTPCACHE_IGNORE_HTTP_CODES': [403, 429],  # Ignore these status codes in the cache
    'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',


    # Set log level to reduce console output
    'LOG_LEVEL': 'INFO'
    }
    
    # 크롤링할 bizId와 cidList를 파일로부터 읽어옵니다.
    data = pd.read_csv("/Users/nojaehyeon/Desktop/workspace/project_4/data/bizid_data_2.csv", index_col=0) # bizId_data
    bizId_list = data['bizId'].tolist()[1729:2323] # 1653:2323, 1692, 1705, 1718, 1729
    cidList_list = data['cidList'].tolist()[1729:2323]
    
    # 전체 리뷰 데이터를 저장할 리스트 초기화
    all_reviews = []
    review_count = 0  # 저장된 리뷰 수를 관리할 변수

    def start_requests(self):
        """각 식당별 첫 페이지 요청을 생성합니다."""
        # bizId와 cidList를 사용하여 첫 페이지의 리뷰 데이터를 요청합니다.
        for biz_id, cid_list in zip(self.bizId_list, self.cidList_list):
            url = "https://pcmap-api.place.naver.com/graphql"
            headers, data_payload = self.prepare_request_data(biz_id, cid_list, 1)

            # meta 데이터로 biz_id, cid_list, page 정보를 전달합니다.
            meta_data = {'biz_id': biz_id, 'cid_list': cid_list, 'page': 1}

            # POST 요청 생성
            yield scrapy.Request(
                url=url,
                method='POST',
                body=json.dumps(data_payload),
                headers=headers,
                callback=self.parse_reviews,
                meta=meta_data
            )

    def prepare_request_data(self, biz_id, cid_list, page):
        """Request 데이터와 헤더를 준비합니다. get_review_data 함수에 해당하는 구조를 정의합니다."""
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko',
            'Content-Type': 'application/json',
            'referer': f'https://pcmap.place.naver.com/restaurant/{biz_id}/review/ugc',
            'Connection': 'keep-alive',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }

        data_payload = [
            {
                "operationName": "getVisitorReviews",
                "variables": {
                    "input": {
                        'businessId': str(biz_id),
                        'businessType': "restaurant",
                        'item': "0",
                        'page': page,
                        'size': 10,
                        'cidList': cid_list,
                    },
                    "getReactions": True,
                    "getTrailer": True,
                    "getUserStats": True,
                    "includeContent": True,
                    "includeReceiptPhotos": True,
                    "isPhotoUsed": False,
                    "item": "0",
                    "page": page,
                    "size": 10,
                    "sort": "recent"
                },
                "query": """
                query getVisitorReviews($input: VisitorReviewsInput) {
                    visitorReviews(input: $input) {
                        items {
                            id
                            reviewId
                            rating
                            author { id nickname }
                            body
                            visited
                            created
                        }
                        total
                    }
                }
                """
            }
        ]

        return headers, data_payload

    def parse_reviews(self, response):
        """첫 페이지의 리뷰 데이터를 파싱하고, 다음 페이지를 요청합니다."""
        biz_id = response.meta['biz_id']
        cid_list = response.meta['cid_list']
        page = response.meta['page']

        # JSON 데이터를 파싱합니다.
        data = json.loads(response.text)

        # 리뷰 데이터가 있는 경우
        if 'errors' not in data and data[0].get('data'):
            reviews = data[0]['data']['visitorReviews']['items']
            total_reviews = data[0]['data']['visitorReviews']['total']
            max_pages = (total_reviews // 10) + 1

            # 리뷰 데이터를 추출하여 리스트에 추가합니다.
            for review in reviews:
                year_num = int(review['visited'].split('.')[0])
                if ( (year_num<13) | (year_num>22) ):
                    author_id = review['author']['id']
                    content = review['body']
                    visited_date = review['visited']
                    created_date = review['created']

                    # 각 리뷰를 딕셔너리 형태로 저장하고, 전체 리뷰 리스트에 추가
                    review_data = {
                        'biz_id': biz_id,
                        'author_id': author_id,
                        'content': content,
                        'visited_date': visited_date,
                        'created_date': created_date
                    }
                    self.all_reviews.append(review_data)
                    self.review_count += 1

                    # 리뷰가 500개 이상일 때 데이터를 저장하고 리스트 초기화
                    if self.review_count >= 500:
                        self.save_reviews()
                        self.all_reviews = []  # 리스트 초기화
                        self.review_count = 0  # 리뷰 수 초기화

            # 다음 페이지가 있는 경우, 다음 페이지를 요청합니다.
            if page < max_pages:
                next_page = page + 1
                headers, data_payload = self.prepare_request_data(biz_id, cid_list, next_page)
                meta_data = {'biz_id': biz_id, 'cid_list': cid_list, 'page': next_page}
                yield scrapy.Request(
                    url="https://pcmap-api.place.naver.com/graphql",
                    method='POST',
                    body=json.dumps(data_payload),
                    headers=headers,
                    callback=self.parse_reviews,
                    meta=meta_data
                )
        else:
            # 데이터가 없거나 오류가 발생한 경우, 'Null' 값을 추가합니다.
            review_data = {
                'biz_id': biz_id,
                'author_id': 'Null',
                'content': 'Null',
                'visited_date': 'Null',
                'created_date': 'Null'
            }
            self.all_reviews.append(review_data)
            self.review_count += 1

    def save_reviews(self):
        """현재까지 수집된 리뷰 데이터를 저장합니다."""
        if self.all_reviews:
            # 모든 리뷰 데이터를 하나의 DataFrame으로 생성
            reviews_df = pd.DataFrame(self.all_reviews)

            # 데이터프레임 생성 및 저장 경로 설정
            save_path = '/Users/nojaehyeon/Desktop/final_project/naver_reviews_all_3.csv'
            # 기존 파일이 있는 경우 이어서 작성하고, 없는 경우 새로 생성합니다.
            if not os.path.exists(save_path):
                reviews_df.to_csv(save_path, index=False, encoding='utf-8-sig')
            else:
                reviews_df.to_csv(save_path, index=False, encoding='utf-8-sig', mode='a', header=False)
            print(f"500개 리뷰 데이터가 {save_path} 경로에 저장되었습니다.")

    def closed(self, reason):
        """크롤링이 종료되면 데이터를 CSV 파일로 저장합니다."""
        # 남아 있는 리뷰가 있을 경우 저장합니다.
        self.save_reviews()
        print(f"모든 리뷰 데이터가 최종 저장되었습니다.")

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ReviewSpider)
    process.start()  # This should only be called once in a single Python process
