# Generated by Django 5.0.3 on 2024-05-07 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_contact_options_ip_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
