from . import models
from django.core.files.base import ContentFile
from .scrapper import *

def run_news_scraper():
    urls = engadged_scrap_urls()
    print('urls got')

    for url in urls:
        if is_new_url(url):
            news = make_news(url)
            print('news got')

            title = make_title(url)
            print('title got')

            category_name = generate_category(news, str(models.Category.objects.all().values_list()))
            category_obj = models.Category.objects.get(name=category_name)
            print('category got')

            image = make_image(news)
            image_file = ContentFile(image, name=f"{url}.jpg")
            print('image got')

            models.News.objects.create(
                title=title,
                text=news,
                category=category_obj,
                banner_image=image_file
            )
            add_url(url)
            print('+1 news')
        else:
            print('skip')