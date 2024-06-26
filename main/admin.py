from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields =  {'slug' : ('title',)}
admin.site.register(models.Category)
# admin.site.register(models.News)
admin.site.register(models.Contact)
admin.site.register(models.Ip_view)
admin.site.register(models.ShortNews)
admin.site.register(models.Reddit_channel)
