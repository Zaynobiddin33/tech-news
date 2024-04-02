from django.shortcuts import render, redirect
from . import models
import requests
from django.core.paginator import Paginator
# Create your views here.


import requests
from django.shortcuts import render

def main(request):
    main = models.News.objects.filter(is_essential = True).order_by('-id').first()
    main3 =models.News.objects.filter(is_essential = True).order_by('-id')[1:4]
    newest5 = models.News.objects.filter(is_essential = False).order_by('-id')[:5]
    news = models.News.objects.all().exclude(id__gte = main3[2].id, is_essential = True)
    all_data = Paginator(news, 9)
    page = request.GET.get('page')
    all = all_data.get_page(page)

    api_key = '32be2340a522e1b2b33f2a0e69cdc3aa'

    # Make a GET request to the OpenWeatherMap API for Tashkent
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Tashkent&appid={api_key}&units=metric'
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant weather data
        city = data['name']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']

        # Pass the weather data to the template
        context = {
            'city': city,
            'temperature': temperature,
            'description': description,
            'main':main,
            'main3':main3,
            'newest5':newest5,
            'all':all
        }
    else:
        # If the request was not successful, display an error message
        context = {
            'error': 'Failed to fetch weather data. Please try again later.',
            'main':main,
            'main3':main3,
            'newest5':newest5,
            'all':all
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
        "id":id
    }
    return render(request, 'category.html', context)


def news(request, id):
    news = models.News.objects.get(id = id)
    recents = models.News.objects.filter().order_by('-id')[:10]
    context = {
        'news':news,
        'recents': recents
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
        'id': id
    }
    return render(request, 'category.html', context)

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