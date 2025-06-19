from bs4 import BeautifulSoup
import requests
from .gemini_check import *
import json
import cloudscraper
import os

address = '51.81.245.3:17981'
proxies = {
        'http':address,
        'https':address
}

def engadged_scrap_urls():
    global proxies
    scraper = cloudscraper.create_scraper()
    url = 'https://arstechnica.com'
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    data = {
        "view": "list"
    }
    response = scraper.post(url, headers=headers, proxies=proxies, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('a', class_='text-gray-700')
    filtered_urls = [url['href'] for url in urls]
    return filtered_urls

def make_title(url):
    scraper = cloudscraper.create_scraper()
    global proxies
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = scraper.get(url, headers=headers, proxies=proxies)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1', class_='dusk:text-gray-100').text
    return generate_title(title)

def make_news(url):
    scraper = cloudscraper.create_scraper()
    global proxies
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = scraper.get(url, headers=headers, proxies=proxies)

    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all('div', class_="post-content")
    text = ''
    for data in body:
        text+=str(data)
    
    return generate_news(text)

def make_image(url):
    scraper = cloudscraper.create_scraper()
    global proxies
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = scraper.get(url, headers=headers, proxies=proxies)
    url = BeautifulSoup(response.text, 'html.parser').find('img', class_='object-cover')['src']

    response = requests.get(url)
    return response.content
    

def is_new_url(url):
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as f:
            urls =  json.load(f)
    else:
        urls = []
        with open('urls.json', 'w')as f:
            json.dump(urls, f)
    return not url in urls

def add_url(url: str):
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as f:
            data = list(json.load(f))
    else:
        data = []

    if url not in data:
        data.append(url)
        with open('urls.json', 'w') as f:
            json.dump(data, f, indent=2)