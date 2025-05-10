from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
import json

MAX_LENGTH = 255

# Модели
class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование коллекции')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    size = models.PositiveIntegerField(default=1, verbose_name='Количество')
    color = models.CharField(max_length=MAX_LENGTH, verbose_name='Цвет')
    photo = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления на сайт')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    collection = models.ManyToManyField(Collection, verbose_name='Коллекция')

    def __str__(self):
        return f"{self.name} - ({self.price} рублей)"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Customer(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Имя')
    last_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderitem_set.all())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    rating = models.IntegerField(verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f"Review for {self.product.name}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Service(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование услуги')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='services/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

# Представления для корзины
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}

    response = redirect('cart_view')
    response.set_cookie('cart', json.dumps(cart))
    return response

@login_required
def remove_from_cart(request, product_id):
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)

    if str(product_id) in cart:
        del cart[str(product_id)]

    response = redirect('cart_view')
    response.set_cookie('cart', json.dumps(cart))
    return response

@login_required
def cart_view(request):
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': item['price']
        })
        total_price += float(item['price']) * item['quantity']

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def create_order(request):
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)
    order = Order.objects.create(user=request.user)

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

    response = redirect('order_detail', order_id=order.id)
    response.set_cookie('cart', json.dumps({}))  # Очистка корзины после создания заказа
    return response

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_price = order.total_price()  # Вычисляем общую стоимость заказа
    return render(request, 'shop/order_detail.html', {'order': order, 'order_items': order_items, 'total_price': total_price})
