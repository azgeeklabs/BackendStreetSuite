# Generated by Django 5.0.6 on 2024-06-10 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0017_alter_answer_options_alter_quizzes_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizzes',
            name='author',
        ),
        migrations.RemoveField(
            model_name='quizzes',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Quizzes',
        ),
    ]
