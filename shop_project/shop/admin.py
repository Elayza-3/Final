from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass