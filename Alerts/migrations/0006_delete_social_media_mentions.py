# Generated by Django 5.0.6 on 2024-07-16 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alerts', '0005_rename_reddit_mentions_social_media_mentions_mentions_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Social_media_mentions',
        ),
    ]