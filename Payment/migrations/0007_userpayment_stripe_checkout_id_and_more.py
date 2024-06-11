# Generated by Django 5.0.6 on 2024-06-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0006_remove_product_price_product_amount_product_price_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='stripe_checkout_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]