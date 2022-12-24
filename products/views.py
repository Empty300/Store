from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from products.models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'products/store.html'
    title = 'Store - Каталог'