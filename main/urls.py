from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('categories', views.category, name = 'category'),
    path('categories/<int:id>', views.category_sorted, name = 'category_sorted'),
    path('news/<str:slug>', views.news, name = 'news'),
    path('contact', views.contact, name = 'contact'),
    path('search', views.search, name = 'search'),
    path('check', views.check, name = 'check'),
    path('check/accept/<int:id>', views.accept, name = 'accept'),
    path('check/deny/<int:id>', views.deny, name = 'deny'),
    path('check/deny/', views.deny, name = 'deny_all'),
    path('getnews/<str:name>', views.get_news, name = 'getnews'),
    path('search_reddit/', views.search_reddit, name = 'search_reddit'),
    path('shorts', views.short_news, name = 'short_news'),
    path('shorts/<str:slug>/', views.short_details, name = 'short_details'),
    path('like-short/<str:slug>', views.like, name = 'like'),
    path('dislike-short/<str:slug>', views.dislike, name = 'dislike')



]