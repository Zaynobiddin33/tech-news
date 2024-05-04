from django.shortcuts import render, redirect
from . import models
import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


import requests
from django.shortcuts import render

from django.core.cache import cache
import requests

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


def news(request, id):
    news = models.News.objects.get(id = id)
    news.views+=1
    news.save()
    recents = models.News.objects.filter().order_by('-id').exclude(id=id)[:10]
    related_news = models.News.objects.filter(category = news.category).exclude(id = id)[:6]
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


