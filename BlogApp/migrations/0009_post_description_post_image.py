# Generated by Django 5.0.6 on 2024-05-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0008_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='', upload_to='PostPic/'),
        ),
    ]