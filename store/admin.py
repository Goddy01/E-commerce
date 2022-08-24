from django.contrib import admin
from .models import Product, Order, OrderItem, BillingAddress, Review
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Review)