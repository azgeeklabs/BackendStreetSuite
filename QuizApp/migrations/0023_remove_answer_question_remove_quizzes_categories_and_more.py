# Generated by Django 5.0.6 on 2024-06-11 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0022_remove_question_difficulty_remove_question_technique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='quizzes',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizzes',
            name='author',
        ),
        migrations.DeleteModel(
            name='UserEmail',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Quizzes',
        ),
    ]
