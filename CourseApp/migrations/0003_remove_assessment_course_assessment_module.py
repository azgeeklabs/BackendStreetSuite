# Generated by Django 5.0.6 on 2024-06-26 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CourseApp', '0002_module_is_completed_alter_course_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='course',
        ),
        migrations.AddField(
            model_name='assessment',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='CourseApp.module'),
        ),
    ]
