from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'
