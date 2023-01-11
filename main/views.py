from django.views.generic import ListView

from common.views import CommonMixin
from products.models import Product


class IndexView(CommonMixin, ListView):
    template_name = 'main/index.html'
    model = Product
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['sale_prod'] = Product.objects.exclude(discount=None).order_by('-discount')[0:7]
        context['random'] = Product.objects.order_by("?")[0:7]
        return context
