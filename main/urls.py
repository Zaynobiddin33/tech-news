from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('categories', views.category, name = 'category'),
    path('categories/<int:id>', views.category_sorted, name = 'category_sorted'),
    path('news/<int:id>', views.news, name = 'news'),



]