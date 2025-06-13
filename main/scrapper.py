from bs4 import BeautifulSoup
import requests
from .gemini_check import *
import json
import os

def engadged_scrap_urls():
    url = 'https://www.engadget.com'
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('a')
    filtered_urls = []
    for url in urls:
        if 'https://www.engadget.com/' in url['href']:
            filtered_urls.append(url['href'])
    sorted_urls = filter_urls(str(filtered_urls))
    return sorted_urls

def make_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('title').text
    return generate_title(title)

def make_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('title').text
    body = soup.find('div', class_="caas-body")
    return generate_news(str(body))

def make_image(news):
    url = BeautifulSoup(news, 'html.parser').find('img')['src']
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