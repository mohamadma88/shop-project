from django.contrib import admin
from . import models


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'is_paid')
    inlines = (OrderItemAdmin,)



@admin.register(models.DiscountCode)
class DiscountCode(admin.ModelAdmin):
    list_display = ('name', 'discount', 'quantity')


