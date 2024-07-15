# Generated by Django 5.0.6 on 2024-07-14 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_id', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=17, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_trial', models.BooleanField(default=False)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_method_id', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Payment.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userpayment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]