from rest_framework import serializers
from shop.models import Category, Collection, Product, Customer, Order, OrderItem, Review, Service, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'name',
            'description'
        ]

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'color',
            'size',
            'photo',
            'create_date',
            'is_exists',
            'collection',
            'category'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone'
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'user',
            'created_at'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'quantity'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'product',
            'customer',
            'rating',
            'comment'
        ]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'name',
            'description',
            'photo'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'user',
            'product',
            'quantity',
            'created_at'
        ]
