from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class News(models.Model):
    title = models.CharField(max_length = 255)
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

