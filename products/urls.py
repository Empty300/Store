from django.urls import path

from products import views
from products.views import ProductsListView, ProductDetailView, FilterListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('filter/', FilterListView.as_view(), name='filter'),
    path('scrap/', views.scrap, name='scrap'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product'),

]
