from django.urls import path

from products import views
from products.views import (ProductDetailView, ProductsListView, basket_add,
                            basket_remove, basket_remove_all, review_add,
                            review_del, CategoriesListView)

app_name = 'products'

urlpatterns = [
    path('filter/', ProductsListView.as_view(), name='filter'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('<int:category_id>/', ProductsListView.as_view(), name='index'),
    path('scrap/', views.scrap, name='scrap'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('baskets/remove_all/', basket_remove_all, name='basket_remove_all'),
    path('review/add/<int:product_id>/', review_add, name='review_add'),
    path('review/del/<int:review_id>/', review_del, name='review_del'),


]
