# Generated by Django 5.0.6 on 2024-05-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0010_post_contentimage_post_time_reading_post_videolink_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AlterField(
            model_name='post',
            name='contentimage',
            field=models.ImageField(blank=True, default='', null=True, upload_to='PostPic/'),
        ),
    ]