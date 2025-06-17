from google import genai
from .tokens import GEMINI_API
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API)

def filter_urls(urls):
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[f"Sort and return the lists of links that possibly be news: {urls}"],
        config={
        "response_mime_type": "application/json",
        "response_schema": list[str],
    },
    )
    return response.parsed


def generate_news(news:str):

    instruction = f'you are a news maker model in uzbek for tech-news.uz website. You are given an information, and you write longer news in uzbek, (no title only news itself, title is already ready) in HTML formatting (not entire html code,it is text formatting only use for links, images, and texts. NO FULL HTML). FORMAT: <p> for each paragraph, <h5> for each subheadings, <img> for images. Use exact same links for <img>s if they exist'

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=False),
            system_instruction=instruction),
            contents=f"{news}",
    )

    return response.text

def generate_title(title:str):

    instruction = 'you are a news maker model in uzbek for tech-news.uz website. you are given a title, and you paraphrase or translate it into Uzbek. Only write title nothing more. Just one title. Not so long, not multiple options. No text styling like markdown, or something. only plain text. No thinking allowed, only give the title'

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=False),
            system_instruction=instruction),
            contents=f"{title}",
    )

    return response.text

def generate_category(news:str, category):
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[f"you are a categorizer model. Write exact name of category from list that is suitable for context of new. LIST: {category}. \n News: {news}"],
        config={
        "response_mime_type": "application/json",
        "response_schema": str,
    },
    )
    return response.parsed

    