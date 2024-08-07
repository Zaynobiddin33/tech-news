from django.shortcuts import render, redirect, get_object_or_404
from . import models
import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import requests
import json
# Create your views here.
from django.core.cache import cache
import praw
import time
from translate import Translator
import html
from . import bot

# from googletrans import Translator

REDDIT_API = 'f0af863c-7380-4f72-b013-e3714699db6f:988ddf50-28fa-4148-9da7-23803484f7be'

def main(request):

    main = models.News.objects.filter(is_essential=True).order_by('-id').first()
    main3 = models.News.objects.filter(is_essential=True).order_by('-id')[1:4]
    newest5 = models.News.objects.filter(is_essential=False).order_by('-id')[:5]
    news = models.News.objects.all().order_by('-id').exclude(id__gte=main3[2].id, is_essential=True)
    all_data = Paginator(news, 9)
    page = request.GET.get('page')
    all = all_data.get_page(page)

    # Check if weather data is cached
    weather_data = cache.get('weather_data')

    # If weather data is not cached or expired, fetch it from the API
    if not weather_data:
        api_key = '32be2340a522e1b2b33f2a0e69cdc3aa'
        url = f'http://api.openweathermap.org/data/2.5/weather?q=Tashkent&appid={api_key}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            description = data['weather'][0]['description']

            # Cache the weather data for an hour
            cache.set('weather_data', {'temperature': temperature, 'description': description}, timeout=3600)
        else:
            # If the request was not successful, set default weather data
            temperature = None
            description = None
    else:
        # Use cached weather data
        temperature = weather_data['temperature']
        description = weather_data['description']

    context = {
        'temperature': temperature,
        'description': description,
        'main': main,
        'main3': main3,
        'newest5': newest5,
        'all': all
    }

    return render(request, 'index.html', context)



def category(request):
    id = 0
    news_raw = models.News.objects.all().order_by('-id')
    p = Paginator(news_raw, 12)
    page = request.GET.get('page')
    news = p.get_page(page)
    context = {
        'news':news,
        'categories': models.Category.objects.all(),
        'id': 'Barcha'
    }
    return render(request, 'category.html', context)


def news(request, slug):
    news = get_object_or_404(models.News, slug=slug)
    news.views+=1
    news.save()
    recents = models.News.objects.filter().order_by('-id').exclude(slug=slug)[:10]
    related_news = models.News.objects.filter(category = news.category).exclude(slug = slug)[:6]
    context = {
        'news':news,
        'recents': recents,
        'all': related_news,
        
    }
    return render(request, 'news.html', context)

def category_sorted(request, id):
    news_raw = models.News.objects.filter(category_id = id).order_by('-id')
    p = Paginator(news_raw, 12)
    page = request.GET.get('page')
    news = p.get_page(page)
    context = {
        'news':news,
        'categories': models.Category.objects.all(),
        'id': models.Category.objects.get(id = id)
    }
    return render(request, 'category.html', context)



@csrf_exempt
def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        models.Contact.objects.create(
            body = message,
            name =name,
            email = email,
        )
    return render(request, 'contact.html')

def search (request):
    q = request.GET.get('q')
    if q:
        news_raw = models.News.objects.filter(Q(title__icontains = q) | Q(text__icontains = q))
    else:
        news_raw = models.News.objects.all()
    p = Paginator(news_raw, 12)
    page = request.GET.get('page')
    news = p.get_page(page)
    context = {
        'news' : news,
        'q':q
    }
    return render(request, 'search.html', context)

@login_required(login_url='main')
def check(request):
    if request.user.is_superuser:
        not_accepted = models.ShortNews.objects.filter(is_accepted = False).order_by('id')
        channels = models.Reddit_channel.objects.all()
    else:
        return redirect('main')
    return render(request, 'check.html', {'not_accepted': not_accepted, 'channels':channels})

@login_required(login_url='main')
def accept(request, id):
    model = models.ShortNews.objects.get(id = id)
    if request.method == 'POST':
        model.is_accepted = True
        model.content = request.POST['text']
        model.save()
    model = models.ShortNews.objects.get(id = id)
    html_text = f'<a href="https://tech-news.uz/shorts/{model.slug}"> Saytda o`qish </a>'
    bot.send_message_sync(model.content + '\n\n 👉🏻' + html_text, image_url=model.image_url)
    return redirect('check')

@login_required(login_url='main')
def deny(request, id=None):
    if id is not None:
        model = models.ShortNews.objects.get(id = id)
    else:
        model = models.ShortNews.objects.filter(is_accepted = False)
    model.delete()
    return redirect('check')

def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translation = translator.translate(text)
    translation = html.unescape(translation)
    return translation

def get_news(request, name):
    REDDIT_CLIENT_ID = '4vyvkbUyrnVfaKQMLj7X5A'
    REDDIT_CLIENT_SECRET = 'vKzSPaHLgpifHObL4La8e2Wa-K8PBA'
    REDDIT_USER_AGENT = 'tech-news-uz by Psychological_Tap676'

    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit_name = name
    subreddit = reddit.subreddit(subreddit_name)
    latest_posts = subreddit.hot(limit=10)

    for num, post in enumerate(latest_posts):
        try:
            image_url = post.preview['images'][0]['source']['url'] if hasattr(post, 'preview') and post.preview else 'None'
        except (AttributeError, IndexError, KeyError):
            image_url = 'None'

        if post.author:
            try:
                redditor = reddit.redditor(post.author.name)
                profile_picture_url = redditor.icon_img
            except Exception as e:
                profile_picture_url = 'None'
                print(f"Error: {e}")
        else:
            profile_picture_url = 'None'
            print("Author not available")

        try:
            content = translate_text(post.title, 'en', 'uz')
        except Exception as e:
            content = 'Translation Error'
            print(f"Translation Error: {e}")

        try:
            models.ShortNews.objects.create(
                image_url=image_url,
                author=post.author.name if post.author else 'Unknown',
                content=content,
                author_pic=profile_picture_url,
                image_height=post.preview['images'][0]['source']['height'] if image_url != 'None' else 0,
                image_width=post.preview['images'][0]['source']['width'] if image_url != 'None' else 0,
                reddit_url=post.shortlink
            )
            print(f'num:{num+1}')
        except Exception as e:
            print(f"Database Error: {e}")
            pass

    return redirect('check')

def short_news(request):
    news_list = models.ShortNews.objects.filter(is_accepted=True).order_by('-id')
    paginator = Paginator(news_list, 10)
    page_number = int(request.GET.get('page', 1))

    news = paginator.get_page(page_number)

    context = {
        'page_obj': news,
        'news': news
    }
    return render(request, 'shorts.html', context)

def search_reddit(request):
    if request.method == 'POST':
        name = request.POST['name']
        # translator = Translator()
        # Replace these values with your own Reddit API credentials
        REDDIT_CLIENT_ID = '4vyvkbUyrnVfaKQMLj7X5A'
        REDDIT_CLIENT_SECRET = 'vKzSPaHLgpifHObL4La8e2Wa-K8PBA'
        REDDIT_USER_AGENT = 'tech-news-uz by Psychological_Tap676'

        # Initialize Reddit instance with your credentials
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Specify the subreddit you want to fetch posts from
        subreddit_name = name
        subreddit = reddit.subreddit(subreddit_name)
        latest_posts = subreddit.hot(limit=10)

        for num, post in enumerate(latest_posts):
            try:
                image_url = post.preview['images'][0]['source']['url'] if hasattr(post, 'preview') and post.preview else 'None'
            except (AttributeError, IndexError, KeyError):
                image_url = 'None'

            if post.author:
                try:
                    redditor = reddit.redditor(post.author.name)
                    profile_picture_url = redditor.icon_img
                except Exception as e:
                    profile_picture_url = 'None'
                    print(f"Error: {e}")
            else:
                profile_picture_url = 'None'
                print("Author not available")

            try:
                content = translate_text(post.title, 'en', 'uz')
            except Exception as e:
                content = 'Translation Error'
                print(f"Translation Error: {e}")

            try:
                if post.media:
                    models.ShortNews.objects.create(
                        image_url=image_url,
                        author=post.author.name if post.author else 'Unknown',
                        content=content,
                        author_pic=profile_picture_url,
                        image_height=post.preview['images'][0]['source']['height'] if image_url != 'None' else 0,
                        image_width=post.preview['images'][0]['source']['width'] if image_url != 'None' else 0,
                        reddit_url=post.shortlink,
                        video = post.media['oembed']['html'],)
                else:
                    models.ShortNews.objects.create(
                        image_url=image_url,
                        author=post.author.name if post.author else 'Unknown',
                        content=content,
                        author_pic=profile_picture_url,
                        image_height=post.preview['images'][0]['source']['height'] if image_url != 'None' else 0,
                        image_width=post.preview['images'][0]['source']['width'] if image_url != 'None' else 0,
                        reddit_url=post.shortlink
                )
                print(f'num:{num+1}')
            except Exception as e:
                print(f"Database Error: {e}")
                pass

        return redirect('check')
    
def short_details(request, slug):
    image = models.ShortNews.objects.get(slug = slug)
    view_key = f'viewed_{image.id}'
    if not request.session.get(view_key, False) and request.method == "GET":
        image.views+=1
        image.save()
        request.session[view_key] = True
    next_news = models.ShortNews.objects.filter(id__lt = image.id).order_by('-id').first()
    prev_news = models.ShortNews.objects.filter(id__gt = image.id).order_by('id').first()
    comments = models.Shorts_comments.objects.filter(short_news = image).order_by('-created_at')
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
    if comments.first() == None:
        comments = None
        num_comments = 0
    else:
        num_comments = comments.count()
    if request.method == 'POST':
        name = request.POST['name']
        comment = request.POST['comment']
        models.Shorts_comments.objects.create(
            creator = name,
            comment = comment,
            short_news = models.ShortNews.objects.get(slug = slug)
        )
    likes = models.Shorts_like.objects.filter(short_news = image).count()
    if models.Shorts_like.objects.filter(short_news = image, user = user_ip).first() == None:
        is_liked = False
    else:
        is_liked = True
    
    return render(request, 'test.html', {'image': image, 'next': next_news, 'prev':prev_news, 'comments':comments, 'num_comments':num_comments, 'is_liked':is_liked, 'likes':likes})

def like(request, slug):
    news = models.ShortNews.objects.get(slug = slug)
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
    models.Shorts_like.objects.create(
        short_news = news,
        user = user_ip
    )
    return redirect('short_details', slug)

def dislike(request, slug):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
    like_obj = models.Shorts_like.objects.get(short_news = models.ShortNews.objects.get(slug = slug), user = user_ip )
    like_obj.delete()
    return redirect('short_details', slug)