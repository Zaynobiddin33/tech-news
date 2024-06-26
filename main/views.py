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

from googletrans import Translator

REDDIT_API = 'f0af863c-7380-4f72-b013-e3714699db6f:988ddf50-28fa-4148-9da7-23803484f7be'

def translation(api_key, text, source_lang, target_lang):    
    url = 'https://mohir.ai/api/v1/translate'
    data = {
        "text": text,
        "src": source_lang,
        "tgt": target_lang,
        "blocking": "true",
        # "webhook_notification_url": "https://example.com"
    }
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "Request timed out. The API response took too long to arrive."

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
        not_accepted = models.ShortNews.objects.filter(is_accepted = False).order_by('-id')
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
    return redirect('check')

@login_required(login_url='main')
def deny(request, id=None):
    if id is not None:
        model = models.ShortNews.objects.get(id = id)
    else:
        model = models.ShortNews.objects.filter(is_accepted = False)
    model.delete()
    return redirect('check')

def get_news(request, name):
    translator = Translator()
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
    subreddit_name = name  # Replace with your desired subreddit

    # Get the subreddit instance
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch the latest posts
    latest_posts = subreddit.hot(limit=30)
    for post in latest_posts:
    # print(post.title)  # Print titles of posts
    # print(post.url)    # Print URLs of posts
    # print('-' * 40)    # Separator between posts
    # translation = translator.translate(post.title, src='en', dest='uz')
    # print(translation)
    # print('-'*50)
        try:
            # Check if the 'preview' attribute exists and access its 'url' if available
            if hasattr(post, 'preview') and post.preview:
                print(post.preview['images'][0]['source']['url'])
            else:
                print('None')  # Print 'None' if 'preview' or its parts are missing
        except AttributeError:
            print('None')  # Handle AttributeError if 'post' does not have 'preview'
        except (IndexError, KeyError):
            print('None')  # Handle IndexError or KeyError if nested attributes are missing

        if post.author:
                try:
                    redditor = reddit.redditor(post.author.name)
                    profile_picture_url = redditor.icon_img
                    print(f"Author's Profile Picture URL: {profile_picture_url}")
                except praw.exceptions.APIException as e:
                    print(f"API Exception: {e}")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("Author not available")

        result = translation(REDDIT_API, post.title, 'en', 'uz')
        print(result['result']['text'])
        try:
            models.ShortNews.objects.create(
                image_url = post.preview['images'][0]['source']['url'],
                author = post.author,
                content = result['result']['text'],
                author_pic = profile_picture_url,
                image_height = post.preview['images'][0]['source']['height'],
                image_width = post.preview['images'][0]['source']['width']
            )
        except:
            pass

    return redirect('check')

def short_news(request):
    news_list = models.ShortNews.objects.filter(is_accepted=True)
    paginator = Paginator(news_list, 30)
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
        translator = Translator()
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
        subreddit_name = name  # Replace with your desired subreddit

        # Get the subreddit instance
        subreddit = reddit.subreddit(subreddit_name)

        # Fetch the latest posts
        latest_posts = subreddit.hot(limit=10)
        for post in latest_posts:
        # print(post.title)  # Print titles of posts
        # print(post.url)    # Print URLs of posts
        # print('-' * 40)    # Separator between posts
        # translation = translator.translate(post.title, src='en', dest='uz')
        # print(translation)
        # print('-'*50)
            try:
                # Check if the 'preview' attribute exists and access its 'url' if available
                if hasattr(post, 'preview') and post.preview:
                    print(post.preview['images'][0]['source']['url'])
                else:
                    print('None')  # Print 'None' if 'preview' or its parts are missing
            except AttributeError:
                print('None')  # Handle AttributeError if 'post' does not have 'preview'
            except (IndexError, KeyError):
                print('None')  # Handle IndexError or KeyError if nested attributes are missing

            if post.author:
                    try:
                        redditor = reddit.redditor(post.author.name)
                        profile_picture_url = redditor.icon_img
                        print(f"Author's Profile Picture URL: {profile_picture_url}")
                    except praw.exceptions.APIException as e:
                        print(f"API Exception: {e}")
                    except Exception as e:
                        print(f"Error: {e}")
            else:
                print("Author not available")

            result = translation(REDDIT_API, post.title, 'en', 'uz')
            print(result['result']['text'])
            if post.media:
                try:
                    models.ShortNews.objects.create(
                    image_url = post.preview['images'][0]['source']['url'],
                    author = post.author,
                    content = result['result']['text'],
                    author_pic = profile_picture_url,
                    image_height = post.preview['images'][0]['source']['height'],
                    image_width = post.preview['images'][0]['source']['width'],
                    video = post.media['oembed']['html']
                )
                except:
                    pass
            else:
                try:
                    models.ShortNews.objects.create(
                    image_url = post.preview['images'][0]['source']['url'],
                    author = post.author,
                    content = result['result']['text'],
                    author_pic = profile_picture_url,
                    image_height = post.preview['images'][0]['source']['height'],
                    image_width = post.preview['images'][0]['source']['width']
                )
                except:
                    pass
        return redirect('check')