# Generated by Django 5.0.3 on 2024-07-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_shortnews_likes_shortnews_shares_shortnews_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortnews',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]