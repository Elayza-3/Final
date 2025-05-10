from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Customer, Product, Category, Collection, Review, Service, CartItem, Order, OrderItem
from .forms import CustomerForm, ProductForm, CategoryForm, CollectionForm, ReviewForm, ServiceForm, RegistrationForm, LoginForm
import json

# Представления для модели Product
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# Представления для модели Category
def categories_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_view')
    else:
        form = CategoryForm()
    return render(request, 'categories.html', {'categories': categories, 'category_form': form})

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories_view')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories_view')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories_view')

# Представления для модели Collection
class CollectionListView(ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collections/collection_detail.html'
    context_object_name = 'collection'

class CollectionCreateView(CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('collection_list')

class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('collection_list')

class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'collections/collection_confirm_delete.html'
    success_url = reverse_lazy('collection_list')

# Представления для модели Review
class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

# Представления для модели Service
def services_view(request):
    services = Service.objects.all()
    reviews = Review.objects.all()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('services_view')
    else:
        form = ServiceForm()
    return render(request, 'services.html', {'services': services, 'service_form': form, 'reviews': reviews})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'shop/order_detail.html', {'order': order, 'order_items': order_items})

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services_view')

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services_view')

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('services_view')

# Представления для модели Customer
class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# Представления для корзины
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.COOKIES.get('cart', '{}')

    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

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

    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    if str(product_id) in cart:
        del cart[str(product_id)]

    response = redirect('cart_view')
    response.set_cookie('cart', json.dumps(cart))
    return response

@login_required
def cart_view(request):
    cart = request.COOKIES.get('cart', '{}')

    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
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

    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    order = Order.objects.create(user=request.user)

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

    response = redirect('order_detail', order_id=order.id)
    response.set_cookie('cart', json.dumps({}))  # Очистка корзины после создания заказа
    return response

def info_view(request):
    return render(request, 'info.html')

def contact_view(request):
    return render(request, 'contact.html')

def about_view(request):
    reviews = Review.objects.all()
    review_form = ReviewForm()
    return render(request, 'about.html', {'reviews': reviews, 'review_form': review_form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('info_view')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'auth/login.html', context)

def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            login(request, form.save())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('info_view')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'auth/registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('info_view')
