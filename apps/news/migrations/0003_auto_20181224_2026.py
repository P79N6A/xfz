# Generated by Django 2.1.4 on 2018-12-24 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-pub_time']},
        ),
    ]
