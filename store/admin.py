from django.contrib import admin
from .models import Product, Order, OrderItem, BillingAddress, Review, UsersRecentlyViewedProduct
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Review)
admin.site.register(UsersRecentlyViewedProduct)