# Generated by Django 5.0.6 on 2024-07-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alerts', '0018_alert_13f_earning_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='market_capital',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
