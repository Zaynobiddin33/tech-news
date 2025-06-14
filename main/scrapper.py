from bs4 import BeautifulSoup
import requests
from .gemini_check import *
import json
import os

def engadged_scrap_urls():
    url = 'https://arstechnica.com'
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('a', class_='uppercase')
    filtered_urls = [url['href'] for url in urls]
    return filtered_urls

def make_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1', class_='dusk:text-gray-100').text
    return generate_title(title)

def make_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all('div', class_="post-content")
    text = ''
    for data in body:
        text+=str(data)
    
    return generate_news(text)

def make_image(url):
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
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