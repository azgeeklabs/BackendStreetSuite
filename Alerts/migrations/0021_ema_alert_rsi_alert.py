# Generated by Django 5.0.6 on 2024-07-21 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alerts', '0020_merge_20240721_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMA_Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy', models.CharField(max_length=50)),
                ('strategy_time', models.CharField(blank=True, max_length=5, null=True)),
                ('ema_value', models.FloatField(blank=True, null=True)),
                ('risk_level', models.CharField(max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ema_alert', to='Alerts.ticker')),
            ],
        ),
        migrations.CreateModel(
            name='Rsi_Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy', models.CharField(max_length=50)),
                ('strategy_time', models.CharField(blank=True, max_length=5, null=True)),
                ('rsi_value', models.FloatField(blank=True, null=True)),
                ('risk_level', models.CharField(max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rsi_alert', to='Alerts.ticker')),
            ],
        ),
    ]
