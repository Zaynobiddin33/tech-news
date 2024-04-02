from django.shortcuts import render, redirect
from . import models

# Create your views here.

def main(request):
    main = models.News.objects.filter(is_essential = True).order_by('-id').first()
    main3 =models.News.objects.filter(is_essential = True).order_by('-id')[1:4]
    newest5 = models.News.objects.filter(is_essential = False).order_by('-id')[:5]
    all = models.News.objects.all().exclude(id__gte = main3[2].id, is_essential = True)
    context = {
        'main':main,
        'main3':main3,
        'newest5':newest5,
        'all':all
    }
    return render(request, 'index.html', context)


def category(request):
    id = 0
    news = models.News.objects.all().order_by('-id')
    context = {
        'news':news,
        'categories': models.Category.objects.all(),
        "id":id
    }
    return render(request, 'category.html', context)


def news(request, id):
    news = models.News.objects.get(id = id)
    context = {
        'news':news
    }
    return render(request, 'news.html', context)

def category_sorted(request, id):
    news = models.News.objects.filter(category_id = id).order_by('-id')
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