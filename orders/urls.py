from django.contrib.auth.views import LogoutView
from django.urls import path

from django.contrib.auth.decorators import login_required

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, stripe_webhook_view, OrderListView, \
    OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),

]