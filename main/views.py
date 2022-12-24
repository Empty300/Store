from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from products.models import Product


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Product
    title = 'Store - Каталог'