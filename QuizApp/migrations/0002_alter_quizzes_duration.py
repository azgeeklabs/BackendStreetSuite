# Generated by Django 5.0.6 on 2024-06-09 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='duration',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]