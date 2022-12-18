from django.contrib import admin
from django.urls import path, include

from products.views import ProductsListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),

]
