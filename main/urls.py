from django.contrib import admin
from django.urls import include, path

from main import settings
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

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
