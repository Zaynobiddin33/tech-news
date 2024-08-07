# Generated by Django 5.0.3 on 2024-07-02 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_shorts_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortnews',
            name='likes',
        ),
        migrations.CreateModel(
            name='Shorts_like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('short_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shortnews')),
            ],
            options={
                'unique_together': {('short_news', 'user')},
            },
        ),
    ]
