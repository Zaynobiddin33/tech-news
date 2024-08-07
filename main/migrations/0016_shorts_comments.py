# Generated by Django 5.0.3 on 2024-07-02 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_shortnews_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shorts_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.TextField()),
                ('short_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shortnews')),
            ],
        ),
    ]
