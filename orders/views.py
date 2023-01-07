from http import HTTPStatus

import stripe
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from main import settings
from orders.forms import OrderForm
from products.models import Basket
from users.forms import UserProfileForm
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Store - Спасибо за заказ!'

class OrderCreateView(CreateView):
    template_name = 'orders/checkout.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1MD3dpAgqawMQZH9nVsViOLr',
                    'quantity': 1,
                },
            ],
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)