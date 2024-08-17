from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    address = models.TextField(blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    size = models.CharField(max_length=15, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)


class DiscountCode(models.Model):
    name = models.CharField(max_length=10,unique=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name
