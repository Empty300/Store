from django.contrib import admin
from django.urls import path, include

from main.views import IndexView
from orders.views import stripe_webhook_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('accounts/', include('allauth.urls')),
    path('webhook/stripe', stripe_webhook_view, name='stripe_webhook')
]

