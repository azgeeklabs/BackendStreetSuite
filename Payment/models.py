from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    price_id = models.CharField(max_length=100,blank=True, null=True)
    title = models.CharField(max_length=17,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    description = models.TextField()
class UserPayment(models.Model):
    user = models.OneToOneField(User, related_name='userpayment', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    free_trial = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method_id = models.CharField(max_length=255, blank=True, null=True)
    


