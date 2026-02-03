from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    sell_price = models.FloatField(default=0.0)
    purchase_price = models.FloatField(default=0.0)
    qty = models.IntegerField()
    min_stock = models.IntegerField(default=5)
    date = models.DateField()

    def __str__(self):
        return self.name


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    total_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
