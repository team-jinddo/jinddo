import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote
import time
import random

# Global lists for storing data
bizId_list = []
res_type_list = []
cidlist_list = []

# Base URL for Naver search
base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="

# User-Agent 리스트
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

# Function to fetch web page text
def get_req_text(url, headers):
    req = requests.get(url, headers=headers)
    status_code = req.status_code
    return req.text, status_code

# Function to extract bizId, cidlist, and res_type from HTML
def get_items(req_text):
    match_bizId = re.search(r'"bizId":"(\d+)"', req_text)
    bizId = match_bizId.group(1) if match_bizId else 'Null'

    match_cidlist = re.search(r'"defaultCategoryCodeList":\s*(\[[^\]]*\])', req_text)
    cidlist = match_cidlist.group(1) if match_cidlist else 'Null'

    soup = BeautifulSoup(req_text, 'html.parser')
    tmp = soup.select_one('span.lnJFt')
    res_type = tmp.get_text() if tmp else 'Null'

    return bizId, cidlist, res_type

# Main function to manage requests
def fetch_data(res_list, start_index=0):
    global bizId_list, res_type_list, cidlist_list
    i = start_index

    while i < len(res_list):
        res_name = res_list[i]
        query = quote(res_name)
        url = base_url + query

        headers = {
            'Referer': f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={query}',
            'Accept-Language': 'ko',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': random.choice(user_agents)
        }

        try:
            req_text, status_code = get_req_text(url, headers)

            if status_code == 200:
                bizId, cidlist, res_type = get_items(req_text)

                res_type_list.append(res_type)
                bizId_list.append(bizId)
                cidlist_list.append(cidlist)

                print(f"Success: {i} | Status Code: {status_code}")

            elif status_code in [403, 429]:
                print(f"Error {status_code} at index {i}. Waiting for 62 minutes...")
                time.sleep(62 * 60)
                continue

            else:
                print(f"Failed: {i} | Status Code: {status_code}")
                break

        except Exception as e:
            print(f"Exception occurred at index {i}: {e}")
            break

        i += 1

        if i % 10 == 0:
            print(f"Processed: {i} items so far.")

        time.sleep(random.uniform(0.15, 0.5))

    print("Completed processing all requests.")
    return bizId_list, res_type_list, cidlist_list