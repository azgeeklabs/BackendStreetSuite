# Generated by Django 5.0.6 on 2024-06-04 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0017_filter_remove_post_tags_post_filters_delete_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='text',
            field=models.CharField(max_length=16),
        ),
    ]