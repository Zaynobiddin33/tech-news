# Generated by Django 5.0.3 on 2024-07-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_shortnews_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortnews',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shortnews',
            name='shares',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shortnews',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]