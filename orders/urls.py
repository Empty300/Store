from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView,
                          OrderDetailView, OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),

]
