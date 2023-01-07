from django.contrib.auth.views import LogoutView
from django.urls import path

from django.contrib.auth.decorators import login_required

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView

app_name = 'orders'

urlpatterns = [
    # path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderCreateView.as_view(), name='order_create'),
    # # path('orders/', OrdersView.as_view(), name='orders'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    ]