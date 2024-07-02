from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import os
from django.conf import settings
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class News(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    text = RichTextUploadingField()
    is_essential = models.BooleanField(default = False)
    banner_image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add = True)
    views = models.IntegerField(default = 0)
    def __str__(self) -> str:
        return self.title
    

        


class Contact(models.Model):
    body = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_checked = models.BooleanField(default=False)
    status = models.CharField(max_length = 1, default = '0')
    sent_time = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = 'message'

class Ip_view(models.Model):
    ip = models.CharField(max_length = 40)
    news = models.ForeignKey(News, on_delete = models.CASCADE)

class ShortNews(models.Model):
    image_url = models.URLField(null=True)
    is_accepted = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    content = models.TextField(unique=True)
    author_pic = models.URLField(null=True, default=None)
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    video = models.TextField(null=True)
    views = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, unique=True)
    reddit_url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        elif self.pk:
            news = ShortNews.objects.get(pk = self.pk)
            if news.content != self.content:
                self.slug = slugify(self.content)
        super(ShortNews, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.content

class Reddit_channel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class Shorts_comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.TextField()
    short_news = models.ForeignKey(ShortNews, on_delete=models.CASCADE)

class Shorts_like(models.Model):
    short_news = models.ForeignKey(ShortNews, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)

    class Meta:
        unique_together = ('short_news', 'user')

    def __str__(self) -> str:
        return self.user