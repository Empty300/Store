from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class ProductsListView(TemplateView):
    template_name = 'products/store.html'
