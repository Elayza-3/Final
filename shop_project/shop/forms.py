from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Category, Product, Collection, Review, Service, Customer, CartItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'size', 'color', 'photo', 'is_exists', 'category', 'collection']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'customer', 'rating', 'comment']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'photo']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
