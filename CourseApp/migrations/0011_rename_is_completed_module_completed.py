# Generated by Django 5.0.6 on 2024-06-27 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CourseApp', '0010_module_is_completed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='is_completed',
            new_name='completed',
        ),
    ]
